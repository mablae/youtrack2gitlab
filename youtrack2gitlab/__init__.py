# youtrack2gitlab

import gitlab
import json

from pprint import pprint

config = {}
with open('config.json') as config_file:
    config = json.load(config_file)
