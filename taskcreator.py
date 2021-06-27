import logging
import logging.config
import re

from jira import JiraTask, RepositoryBranch


class TaskCreator:
    def __init__(self, all_branches, config_dict):
        logging.config.dictConfig(config_dict)
        self._logger = logging.getLogger(__name__)
        self._branches = all_branches

    def create_tasks_from_list(self, tasks_data):
        jira_tasks = []
        has_no_errors = True
        for row in tasks_data:
            try:
                jira_tasks.append(self._create_task(row))
            except Exception:
                has_no_errors = False
        if has_no_errors:
            return jira_tasks
        raise Exception("Tasks data contains errors")

    def _create_task(self, row):
        values_dist = self._try_to_parse_values(row)
        return JiraTask(values_dist["name"], values_dist["branches"],
                        values_dist["templates"])

    def _try_to_parse_values(self, row):
        is_successful_parse = True
        values_dist = {"name": None, 'branches': [], 'templates': []}
        parse_methods = [self._get_task_name, self._get_branches,
                         self._get_templates]
        for value, method in zip(values_dist, parse_methods):
            try:
                parsed_values[value] = method()
            except Exception as ex:
                self._logger.exception(ex)
                is_successful_parse = False
        if is_successful_parse:
            return values_dist
        raise Exception("Parse values from row has failed")

    def _get_task_name(self, row):
        task_name_pattern = r'NEED_PATTERN'
        if re.match(task_name_pattern, row[0]) is not None:
            return row[0]
        raise Exception(f"Task name value: '{row[0]}' is not match to pattern")

    def _get_branches(self, row):
        branch_pattern = r'https://git\.promedweb\.ru/rtmis/' \
                         r'(report_(ms|pg))/-/tree/([A-Z]-\d+)'
        failed_values = []
        branches = []
        delimiters = re.compile(r'\s*[;,]?\n?\s*')
        for value in delimiters.split(row[1]):
            branch = re.match(template_pattern, value)
            if branch:
                repository_name = branch.group(1)
                branch_name = branch.group(2)
                branches.append(RepositoryBranch(repository_name, branch_name))
            else:
                failed_values.append(value)
        if failed_values:
            raise Exception(f"Branch name values: {failed_values} "
                            f"is not match to pattern")

    def _get_templates(self, row):
        template_pattern = r'NEED_PATTERN'
        failed_values = []
        templates = []
        delimiters = re.compile(r'\s*[;,]?\n?\s*')
        for value in delimiters.split(row[2]):
            template = re.match(template_pattern, value)
            if template:
                templates.append(template)
            else:
                failed_values.append(value)
        if failed_values:
            raise Exception(f"Template name values: {failed_values} "
                            f"is not match to pattern")
