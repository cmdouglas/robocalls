from flask import render_template, request, flash

from app import app
from app.forms import MakeCallForm
from app.person import persist_user
from app.representatives import get_reps_by_postal_code
from app.call import make_calls


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = MakeCallForm()
    if request.method == 'POST' and form.validate_on_submit():
        persist_user(
            form.email.data,
            form.given_name.data,
            form.family_name.data,
            form.postal_code.data
        )

        reps = get_reps_by_postal_code(form.postal_code.data)
        for rep in reps:
            flash(f"I would have called {rep['name']} at {rep['phone']}")


        make_calls(reps)

        return render_template('confirmation.html')

    return render_template('index.html', form=form)


@app.route('/confirmation')
def confirmation():
    pass
