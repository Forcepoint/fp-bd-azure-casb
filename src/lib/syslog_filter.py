#
# Author:  Dlo Bagari
# created Date: 03-12-2019


class SyslogFilter:
    def __init__(self, settings, logger):
        self._settings = settings
        self._logger = logger

    def get_filters(self):
        """
        generate syslog-ng filter functions according th settings requirements and return them
        :return: filter_functions, error
        """
        filters = []
        filters_name = []
        filter_parameters = self._settings.get("logs_filter_parameters")
        if filter_parameters is not None and len(filter_parameters) != 0:
            for parameter in filter_parameters:
                if parameter == "include":
                    for key in filter_parameters[parameter]:
                        values = filter_parameters[parameter][key].strip().split(',')
                        if len(values) != 0:
                            matches = []
                            for i in values:
                                matches.append(f"match('{i.strip()}')")
                            join_matches = " or ".join(matches)
                            filter_name = f"{key}_filter"
                            filters_name.append(filter_name)
                            filter_definition = 'filter %s {%s ;};' % (filter_name, join_matches)
                            filters.append(filter_definition)
                elif parameter == "exclude":
                    for key in filter_parameters[parameter]:
                        values = filter_parameters[parameter][key].strip().split(',')
                        if len(values) != 0:
                            matches = []
                            for i in values:
                                matches.append(f"not match('{i.strip()}')")
                            join_matches = " or ".join(matches)
                            filter_name = f"{key}_filter"
                            filters_name.append(filter_name)
                            filter_definition = 'filter %s {%s ;};' % (filter_name, join_matches)
                            filters.append(filter_definition)
        return filters, filters_name



