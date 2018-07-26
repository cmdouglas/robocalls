from datetime import timedelta

from flask import render_template, request, session, redirect, url_for

from app import app
from app.forms import MakeCallForm
from app.representatives import get_reps_by_postal_code
from app.jobs import make_calls_job, persist_person_job


@app.before_request
def session_timeout():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = MakeCallForm()
    if request.method == 'POST' and form.validate_on_submit():
        reps = get_reps_by_postal_code(form.postal_code.data)

        session['reps'] = reps
        session['given_name'] = form.given_name.data
        session['family_name'] = form.family_name.data
        session['postal_code'] = form.postal_code.data

        persist_person_job.delay(
            form.email.data,
            form.given_name.data,
            form.family_name.data,
            form.postal_code.data,
        )

        make_calls_job.delay(
            form.given_name.data,
            form.family_name.data,
            form.postal_code.data,
            reps
        )

        return redirect(url_for('confirmation', _anchor="share"))

    return render_template('index.html', form=form)


@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    reps = session.get('reps', None)

    given_name = session.get('given_name', None)
    family_name = session.get('family_name', None)
    postal_code = session.get('postal_code', None)

    if not reps:
        return redirect(url_for('index'))

    if request.method == 'POST':
        make_calls_job.delay(
            given_name,
            family_name,
            postal_code,
            reps
        )

    return render_template('confirmation.html', reps=reps)
