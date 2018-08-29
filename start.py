'''
start.py

This is the starting point for the pibs_client.
To run:
$ pip install -r requirements.txt  (1st time only)
$ python start.py

- Scott Null, 08/23/18
'''

from definitions import *
# update the package map
from tools import updateDirInit
updateDirInit('./sensors',iterative=True)
updateDirInit('./tasks',iterative=True)
from core import Node
import json

with open(LOCAL_CONFIG_FILE,'rb') as f:
    sys_json = f.read()

system_dict = json.loads(sys_json)
node = Node(system=system_dict)
node.loop_start()
