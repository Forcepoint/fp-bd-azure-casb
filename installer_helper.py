#
# Author:  Dlo Bagari
# created Date: 03-12-2019

from sys import argv
import yaml
from os import system

config_file = argv[1]
with open(config_file) as f:
    data = yaml.load(f, yaml.SafeLoader)
    target_directory = data["application_directory"]
    cmd = "sudo mkdir -p {}".format(target_directory)
    system(cmd)
    cmd2 = "sudo chmod 777 {}".format(target_directory)
    system(cmd2)
    log_directory = data["logs_directory"]
    cmd = "sudo mkdir -p {}".format(log_directory)
    system(cmd)
    cmd2 = "sudo chmod 777 {}".format(log_directory)
    system(cmd2)
    siem_tool_outputs_location = data["SIEM_tool_outputs_location"]
    start_time_files = ['service_provider_logs/activities_last_run.txt', 'service_provider_logs/alerts_last_run.txt',
                        'realtime_monitoring/activities_last_run.txt', 'realtime_monitoring/alerts_last_run.txt',
                        'admin_audit/activities_last_run.txt', 'incidents/incidents_last_run.txt']
    for file in start_time_files:
        system(f"mkdir -p {siem_tool_outputs_location}/{file.split('/')[0]}")
        system(f"touch {siem_tool_outputs_location}/{file}")
    print(target_directory)