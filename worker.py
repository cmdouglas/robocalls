from rq import Worker, Queue, Connection
from rq.handlers import move_to_failed_queue
from app import app
from app.jobs import conn

listen = ['default']



if __name__ == '__main__':
    with Connection(conn):
        app.logger.info('HELLO')
        worker = Worker(map(Queue, listen))
        worker.work()
