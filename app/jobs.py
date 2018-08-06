from rq.decorators import job

from app import redis_connection
from app.people import persist_person
from app.calls import make_calls


@job('default', connection=redis_connection)
def persist_person_job(person):
    persist_person(person)


@job('default', connection=redis_connection)
def make_calls_job(person, reps):
    make_calls(person, reps)
