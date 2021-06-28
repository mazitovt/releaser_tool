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
        parse_methods = [TaskCreator._get_task_name, self._get_branches,
                         TaskCreator._get_templates]
        for value, method in zip(values_dist, parse_methods):
            try:
                parsed_values[value] = method()
            except Exception as ex:
                self._logger.exception(ex)
                is_successful_parse = False
        if is_successful_parse:
            return values_dist
        raise Exception("Parse values from row has failed")

    @staticmethod
    def _get_task_name(row):
        task_name_pattern = r'[A-Z]+-\d+'
        if re.match(task_name_pattern, row[0]) is not None:
            return row[0]
        raise Exception(f"Task name value: '{row[0]}' is not match to pattern")

    def _get_branches(self, row):
        branch_pattern = r'https://git\.promedweb\.ru/rtmis/' \
                         r'(report_(ms|pg))/-/tree/([A-Z]+-\d+)'
        failed_values = []
        not_existed_branches = []
        branches = []
        delimiters = re.compile(r'\s*[;,]?\n?\s*')
        for value in delimiters.split(row[1]):
            branch = re.match(branch_pattern, value)
            if branch:
                repository_name = branch.group(1)
                branch_name = branch.group(2)
                branches.append(RepositoryBranch(repository_name, branch_name))
            else:
                failed_values.append(value)
        for branch in branches:
            if not branch.is_contained_in(self._branches):
                not_existed_branches.append()
        if not_existed_branches or failed_values:
            error_message = ""
            if not_existed_branches:
                error_message = f"Branches: {not_existed_branches} " \
                                f"are not exists"
            if failed_values:
                error_message += f"Branch name values: {failed_values} " \
                                 f"are not match to pattern"
            raise Exception(error_message)
        if not branches:
            raise Exception("Branches are not found")
        return branches

    @staticmethod
    def _get_templates(row):
        template_pattern = r'(?<=(\d{1,3}/)?)[a-zA-Z_-0-9]+\.rptdesign]'
        # 59/r59_template.rptdesign
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
        if not templates:
            raise Exception("Templates are not found")
        return templates
