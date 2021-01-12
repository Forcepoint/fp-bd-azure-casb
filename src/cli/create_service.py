#
# Author:  Dlo Bagari
# created Date: 03-12-2019

import subprocess
import yaml
from subprocess import Popen
from os import system, path


class CreateService:
    def __init__(self, parser):
        self._parser = parser
        self._args = None
        self._settings = None

    def __call__(self, args):
        self._args = args
        with open(self._args.config_file) as f:
            self._settings = yaml.load(f, yaml.SafeLoader)
        result = self.is_service_exists(self._args.name)
        if result is True:
            self._parser.error("The service '{}' is already exists".format(self._args.name))
        else:
            self._create_service(self._args.name)
        if self._args.start is True:
            result, error_code = self.is_service_running(self._args.name)
            if error_code == 1:
                self._parser.error("problem with executing commands")
            if error_code == 0 and result is True:
                self._parser.error("The service '{}' is already running".format(self._args.name))
            system("systemctl daemon-reload")
            if self._args.start is True:
                system("systemctl start {}.service".format(self._args.name))

    @staticmethod
    def execute_cmd(cmd):
        process = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, errors = process.communicate()
        return output, errors

    def is_service_exists(self, name):
        service_path = "/etc/systemd/system/{}.service".format(name)
        return path.isfile(service_path)

    def is_service_running(self, name):
        cmd = ["systemctl",  "list-units"]
        output, errors = self.execute_cmd(cmd)
        output = output.strip()
        if len(output) != 0:
            output = output.split("\n")
            for line in output:
                if line.strip().startswith("{}.service ".format(name)):
                    return True, 0
            return False, 0
        return False, 1

    def _create_service(self, name):
        service = """
[Unit]
Description= run azure_casb.service
Requires=syslog-ng.service
After=syslog-ng.service

[Service]
ExecStart={}/scripts/azure_casb.sh run -c {}

[Install]
WantedBy=multi-user.target
""".format(self._settings["application_directory"], self._settings["application_directory"] + "/settings.yml")
        service_path = "/etc/systemd/system/{}.service".format(name)
        with open(service_path, "w") as f:
            f.write(service)
        system("chmod 644 {}".format(service_path))
        system("systemctl daemon-reload")
