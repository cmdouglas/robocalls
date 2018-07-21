from datetime import timedelta

from flask import render_template, request, session, redirect, url_for

from app import app
from app.forms import MakeCallForm
from app.people import create_person
from app.representatives import get_reps_by_postal_code
from app.calls import make_calls


@app.before_request
def session_timeout():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = MakeCallForm()
    if request.method == 'POST' and form.validate_on_submit():
        create_person(
            form.email.data,
            form.given_name.data,
            form.family_name.data,
            form.postal_code.data
        )

        session['given_name'] = form.given_name.data
        session['family_name'] = form.family_name.data
        session['postal_code'] = form.postal_code.data

        reps = get_reps_by_postal_code(form.postal_code.data)
        make_calls(form.given_name.data, form.family_name.data, form.postal_code.data, reps)

        return redirect(url_for('confirmation'))

    return render_template('index.html', form=form)


@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    family_name = session.pop('family_name', None)
    given_name = session.pop('given_name', None)
    postal_code = session.pop('postal_code', None)

    if not (given_name and family_name and postal_code):
        return redirect(url_for('index'))

    if request.method == 'POST':
            reps = get_reps_by_postal_code(postal_code)
            make_calls(app, given_name, family_name, postal_code, reps)

    return render_template('confirmation.html')
