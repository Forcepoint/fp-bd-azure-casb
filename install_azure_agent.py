#
# Author:  Dlo Bagari
# created Date: 03-12-2019

import yaml
from os import system
from sys import argv

config_file = argv[1]
with open(config_file) as f:
    data = yaml.load(f, yaml.SafeLoader)
    system(data["log_azure_agent"])
