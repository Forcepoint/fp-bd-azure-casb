import yaml
import glob
from os import system


class Credentials:
    def __init__(self, parser):
        self._parser = parser
        self._args = None
        self._settings = None

    def __call__(self, args):
        self._args = args
        with open(self._args.config_file) as f:
            self._settings = yaml.load(f, yaml.SafeLoader)
        self._create_credential_file()

    def _create_credential_file(self):
        """
        creates credentials file for SIEM Tool
        :return: None
        """
        # find SIEM tool directory
        siem_tool_directory = glob.glob(f"{self._settings['application_directory']}/SIEM-Tool-Linux*")
        if len(siem_tool_directory) == 0:
            self._parser.error(f"SIEM tool is not exists under {self._settings['application_directory']}")
        if len(siem_tool_directory) > 1:
            self._parser.error(f"multiple SIEM tool directory exist under {self._settings['application_directory']}")
        siem_tool_directory = siem_tool_directory[0]
        cmd = f"cd {siem_tool_directory};./SIEMClient.sh --set.credentials --username '{self._args.username}'" \
              f" --password '{self._args.password}' --credentials.file {siem_tool_directory}/credentials_file"
        system(cmd)


