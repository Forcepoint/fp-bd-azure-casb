# Author:  Dlo Bagari
# created Date: 02-12-2019

import argparse
from .syslog_service import SyslogService
from .create_service import CreateService
from .credentials import Credentials


class CliArgs:
    def __init__(self, name):
        self._parser = argparse.ArgumentParser(prog=name)
        self._syslog_service = SyslogService(self._parser)
        self._create_service = CreateService(self._parser)
        self._credentials = Credentials(self._parser)
        self._build_args()

    def _build_args(self):
        subparsers = self._parser.add_subparsers(title="sub-commands")
        run_cli = subparsers.add_parser("run",
                                        description="Runs azure_casb service")
        run_cli.add_argument("--config-file", "-c", action="store", dest="config_file",
                             help="The config file path", required=True)
        run_cli.add_argument("--start-date", "-s", action="store", dest="start_date",
                             help="the start date for SIEM Tool in format DD-MM-YY")
        run_cli.set_defaults(function=self._syslog_service)
        service_cli = subparsers.add_parser("service", description="create Systemd Service for azure_casb.service")
        service_cli.add_argument("--config-file", "-c", action="store", dest="config_file",
                                 help="the config file path", required=True)
        service_cli.add_argument("--start", "-s", action="store_true",
                                 default=False, dest="start", help="Start systemd service(azure_casb.service)")
        service_cli.add_argument("--name", "-n", action="store",
                                 default="azure_casb", dest="name", help="the service name, "
                                                                         "default name is 'azure_casb'")
        service_cli.set_defaults(function=self._create_service)
        credentials_cli = subparsers.add_parser("credentials", description="creates credentials file")
        credentials_cli.add_argument("--config-file", "-c", action="store", dest="config_file",
                                     help="the config file path", required=True)
        credentials_cli.add_argument("--username", "-u", action="store", dest="username", help="CASB username",
                                     required=True)
        credentials_cli.add_argument("--password", "-p", action="store", dest="password", help="CASB password",
                                     required=True)
        credentials_cli.set_defaults(function=self._credentials)

    def get_parser(self):
        return self._parser
