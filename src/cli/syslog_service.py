#
# Author:  Dlo Bagari
# created Date: 03-12-2019

import yaml
import glob
from os import path, system
from datetime import datetime
from src.lib.syslog_filter import SyslogFilter

SYSLOG_CONFIG_LOCATION = "/etc/syslog-ng/conf.d/security-config-omsagent.conf"


class SyslogService:
    def __init__(self, parser):
        self._args = None
        self._parser = parser
        self._settings = None

    def __call__(self, args):
        self._args = args
        with open(self._args.config_file) as f:
            self._settings = yaml.load(f, yaml.SafeLoader)
        a = SyslogFilter(self._settings, None)
        filters, filters_name = a.get_filters()
        syslog_config = 'filter f_oms_filter {match("CEF\|ASA" ) ;};\n%s\ndestination oms_destination ' \
                        '{tcp("127.0.0.1" port(25226));};\n' \
                        'log {source(s_src);filter(f_oms_filter);%s;destination(oms_destination);};' \
                        % ("\n".join(filters), ";".join(f"filter({i})" for i in filters_name))
        self._set_syslog_config(syslog_config)
        if self._args.start_date is not None:
            self._set_log_starting_date(self._args.start_date, True)
        else:
            self._set_log_starting_date(self._settings["logs_starting_date"])
        self._run()

    def _set_syslog_config(self, syslog_config):
        """
        change the syslog-ng filtering policies and forwarding polices
        :param syslog_config:a new config for syslog-ng
        :return: None
        """
        if path.isfile(SYSLOG_CONFIG_LOCATION) is True:
            with open(SYSLOG_CONFIG_LOCATION) as f:
                config = f.read().strip()
            if config != syslog_config.strip():
                with open(SYSLOG_CONFIG_LOCATION, 'w') as syslog_file:
                    syslog_file.write(f"\n{syslog_config}")
                system("systemctl restart syslog-ng.service")
        else:
            self._parser.error("syslog-ng config file does not exist")

    def _set_log_starting_date(self, start_time, restart_dam=False):
        """
        set the timestamp for SIEM TOOL.
        :return: None
        """
        start_time = str(start_time)
        start_date = None
        try:
            start_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            self._parser.error(e.args[0])
        timestamp = int(datetime.timestamp(start_date))
        # wire the timestamp to all txt files in SIEM_tool_outputs_location
        time_files = glob.glob(f"{self._settings['SIEM_tool_outputs_location']}/*/*.txt")

        for f in time_files:
            # read current time, if no time or time is zero, set the timestamp
            current_time = None
            with open(f) as f_read:
                current_time = f_read.read().strip()
                current_time = current_time.split(':')[0]
            if current_time == "" or int(current_time) == 0:
                with open(f, 'w') as t_file:
                    t_file.write(str(timestamp) + "000")
        if restart_dam is True:
            system("systemctl restart azure_casb.service")

    def _run(self):
        """
        run SIEM tool to query new lof=gs from Forcepoint CASB
        :return: None
        """
        seim_path = f"{self._settings['application_directory']}/SIEM-Tool-Linux*"
        siem_tool_directory = glob.glob(seim_path)
        if len(siem_tool_directory) == 0:
            self._parser.error(f"SIEM tool is not exists under {self._settings['application_directory']}")
        if len(siem_tool_directory) > 1:
            self._parser.error(f"multiple SIEM tool directory exist under {self._settings['application_directory']}")
        siem_tool_directory = siem_tool_directory[0]
        cmd = f'cd {siem_tool_directory};./SIEMClient.sh --credentials.file credentials_file ' \
              f'--output.dir {self._settings["SIEM_tool_outputs_location"]} ' \
              f' --host {self._settings["casb_host"]} --port 443 ' \
              f'  truststorePath={self._settings["application_directory"]}/truststore' \
              f' exportSyslog=true syslogHost=127.0.0.1 syslogFacility=local2 cefCompliance=true'
        if self._settings["include_admin_audit_logs"] is True:
            cmd = cmd + " --admin.audit"
        system(cmd)
