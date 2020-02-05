import json
import logging
import time

import requests

import settings
from redis_worker import RedisWQ
from tenacity import retry
from tenacity.wait import wait_fixed
from tenacity.stop import stop_after_attempt

logger = logging.getLogger('sync-worker')


def _num_running_jobs():
    response = requests.get(settings.STATUS_ENDPOINT, timeout=5)
    if response.status_code == 200:
        result = response.json()
        return int(result.get('running'))
    return settings.MAX_PROCESS_PER_WORKER


def _process_item(job_queue, wait=1):
    logger.debug('Worker with sessionID: {}'.format(job_queue.sessionID()))
    logger.debug('Initial queue state: empty= {}'.format(
        str(job_queue.empty())))

    while True:
        while not job_queue.empty():
            job_queue.check_expired_leases()
            job = job_queue.lease(lease_secs=10, block=True, timeout=5)

            if job is None:
                logger.info("Waiting for work")
                time.sleep(wait)
                continue

            item_str = job.decode('utf-8')
            item = json.loads(item_str)
            logger.debug('Working on {}'.format(item))

            num_running_jobs = _num_running_jobs()
            if num_running_jobs < settings.MAX_PROCESS_PER_WORKER:
                response = requests.post(
                    settings.SCHEDULE_ENDPOINT,
                    data={
                        'project': item.get('project'),
                        'spider': item.get('spider')
                    }
                )
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('status')
                    job_id = result.get('jobid')
                    logger.debug(
                        'job with job_id: {} and status: {} created'.format(job_id, status))
                    if status == 'ok' and job_id is not None:
                        job_queue.complete(item_str.encode('utf-8'))

        logger.info(
            'Job queue finished, witing {} seconds before pulling again.'.format(wait))
        time.sleep(wait)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def _delpoy_project():
    with open('/src/scraperapp/dist/scraperapp-1.0.0-py3.8.egg', 'rb') as egg:
        response = requests.post(
            url=settings.ADD_VERSION_ENDPOINT,
            data={
                'project': 'scraperapp',
                'version': 'r1'
            },
            files={
                'egg': egg
            },
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            return result.get('spiders')
        logger.debug("unable to deploy projcect to scrapy daemon")


def main():
    _delpoy_project()
    q = RedisWQ(
        name=settings.WORKER_QUEUE_NAME,
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD)

    try:
        _process_item(q)
    except KeyboardInterrupt:
        retcode = 0  # ok
    except Exception:
        retcode = 2
    return retcode


if __name__ == "__main__":
    main()
