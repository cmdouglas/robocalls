from rq import Worker, Queue, Connection
from app import redis_connection

listen = ['default']



if __name__ == '__main__':
    with Connection(redis_connection):
        worker = Worker(map(Queue, listen))
        worker.work()
