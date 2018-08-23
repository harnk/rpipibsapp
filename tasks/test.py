import json
import time
import core
from definitions import *

current_milli_time = lambda: int(round(time.time() * 1000))


def echo(node, args):
    print 'TASK: tasks.test.echo(node,args) @time:', current_milli_time(), 'ms'
    """
    task_name = tasks.test.echo'
    arguments = {'message': text_message [str],
                 'topic': mqtt_topic [str]}
    example:
    payload = {'task_name': 'tasks.test.echo',
               'arguments': {'topic': 'rawr', 'echo_text': 'meow'}}
    publish.single("rawr", json.dumps(payload), hostname="127.0.0.1")
    """
    payload = {'echo_text': str(args['echo_text'])}
    node.messenger.publish(str(args[key_topic]), payload=json.dumps(payload))
    time.sleep(1)
