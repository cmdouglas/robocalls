import redis
from rq import Queue

from app import app
from app.people import persist_person
from app.calls import make_calls

conn = redis.from_url(app.config.get('RQ_REDIS_URL'))
q = Queue('default', connection=conn)


def enqueue_job(f, *args):
    job = q.enqueue(f, *args)
    app.logger.info(f'job added: {job}')


def persist_person_job(email, given_name, family_name, postal_code):
    persist_person(email, given_name, family_name, postal_code)


def make_calls_job(given_name, family_name, postal_code, reps):
    make_calls(given_name, family_name, postal_code, reps)
