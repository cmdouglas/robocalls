from datetime import timedelta

from flask import render_template, request, session, redirect, url_for
from dataclasses import asdict

from app import app
from app.models.person import Person
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
        person = Person()
        form.populate_obj(person)
        reps = get_reps_by_postal_code(form.postal_code.data)

        session['reps'] = reps
        session['person'] = asdict(person)
        persist_person_job.delay(
            person
        )

        make_calls_job.delay(
            person,
            reps
        )

        return redirect(url_for('confirmation', _anchor="share"))

    return render_template('index.html', form=form)


@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    reps = session.get('reps', None)
    person_dict = session.get('person', None)

    if not reps:
        return redirect(url_for('index'))

    if request.method == 'POST':
        make_calls_job.delay(
            Person(**person_dict),
            reps
        )

    return render_template('confirmation.html', reps=reps)
