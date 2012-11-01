#!/usr/bin/env python
import time
import json
import redis
import socket
import random


def queue_build_event(action, redis_instance, message=None):
    environment = socket.gethostname()
    event = {'environment': environment,
             'action': action,
             'timestamp': str(time.time()),
             'message': 'Completed deployment of build 3.3.2.2',
             'log_url': 'http://{0}/deployment-logs/'.format(environment)}
    redis_instance.publish("build:events:{0}".format(environment),
                           json.dumps(event))


if __name__ == '__main__':
    r = redis.Redis()
    actions = ['Checked out code', 'Compiled', 'Ran unit tests',
               'Ran config tests', 'Config Errors', 'Stop app server',
               'Deploy code', 'Start app server', 'Run functional tests']
    for action in actions:
        queue_build_event(action, r, message=action)
        time.sleep(random.randrange(2, 10))
