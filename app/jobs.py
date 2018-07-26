from rq.decorators import job

from app import redis_connection
from app.people import persist_person
from app.calls import make_calls


@job('default', connection=redis_connection)
def persist_person_job(email, given_name, family_name, postal_code):
    persist_person(email, given_name, family_name, postal_code)


@job('default', connection=redis_connection)
def make_calls_job(given_name, family_name, postal_code, reps):
    make_calls(given_name, family_name, postal_code, reps)
