import redis
from rq import Queue

from app import app
from app.people import persist_person
from app.calls import make_calls

conn = redis.from_url(app.config.get('RQ_REDIS_URL'))


def enqueue_job(f, *args):
    q = Queue(connection=conn)
    q.enqueue(f, *args)


def save_person_and_make_calls_job(email, given_name, family_name, postal_code, reps):
    persist_person(email, given_name, family_name, postal_code)
    make_calls(given_name, family_name, postal_code, reps)


def make_calls_job(given_name, family_name, postal_code, reps):
    make_calls(given_name, family_name, postal_code, reps)
