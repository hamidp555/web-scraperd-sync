import os

REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT = os.getenv("REDIS_PORT") or "6379"
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
WORKER_QUEUE_NAME = os.getenv("WORKER_QUEUE_NAME")
WORKER_PORT = os.getenv("WORKER_PORT")
WORKER_HOST = os.getenv("WORKER_HOST")
WORKER_SCHEDULE_ENDPOINT = os.getenv("WORKER_SCHEDULE_ENDPOINT")
WORKER_STATUS_ENDPOINT = os.getenv("WORKER_STATUS_ENDPOINT")
WORKER_ADDVERSION_ENDPOINT = os.getenv("WORKER_ADDVERSION_ENDPOINT")
MAX_PROCESS_PER_WORKER = int(os.getenv("MAX_PROCESS_PER_WORKER")) or 4

SCHEDULE_ENDPOINT = 'http://{}:{}/{}'.format(
    WORKER_HOST, WORKER_PORT, WORKER_SCHEDULE_ENDPOINT)
STATUS_ENDPOINT = 'http://{}:{}/{}'.format(
    WORKER_HOST, WORKER_PORT, WORKER_STATUS_ENDPOINT)
ADD_VERSION_ENDPOINT = 'http://{}:{}/{}'.format(
    WORKER_HOST, WORKER_PORT, WORKER_ADDVERSION_ENDPOINT)
