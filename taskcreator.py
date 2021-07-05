import logging
import logging.config
import re
from logger import (LOG_CONF_FILE_PATH, load_json, get_logger)
from jira_task import JiraTask
from repo_branch import RepositoryBranch
from regex_patterns import (match_template_pattern, split_on_delimiters)


class TaskCreator:
    def __init__(self, all_branches):
        log_config = load_json(LOG_CONF_FILE_PATH)
        logging.config.dictConfig(log_config)
        self._logger = get_logger(log_config)
        pass

    def create_tasks_from_list(self, tasks_data):
        jira_tasks = []
        has_no_errors = True
        for task_dict in tasks_data:
            try:
                jira_tasks.append(self._create_task(task_dict))
            except Exception as e:
                self._logger.exception(e)
                has_no_errors = False
        if has_no_errors:
            return jira_tasks
        raise Exception("Tasks data contains errors")

    def _create_task(self, row):
        values_dist = TaskCreator._try_to_parse_values(self._logger,row)
        return JiraTask(
            values_dist["name"], values_dist["branches"], values_dist["templates"]
        )

    @staticmethod
    def _try_to_parse_values(logger, data_dict):
        is_successful_parse = True
        values_dict = {"name": None, "branches": [], "templates": []}

        parse_methods = [
            TaskCreator._get_task_name,
            TaskCreator._get_branches,
            TaskCreator._get_templates
        ]

        for key, method in zip(data_dict.keys(), parse_methods):
            try:
                values_dict[key] = method(data_dict[key])
            except Exception as ex:
                logger.exception(ex)
                is_successful_parse = False
        if is_successful_parse:
            return values_dict
        raise Exception("Parse values from row has failed")

    @staticmethod
    def _get_task_name(str_name):
        task_name_pattern = r"[A-Z]+-\d+"
        if re.match(task_name_pattern, str_name) is not None:
            return str_name
        raise Exception(f"Task name value: '{str_name}' is not match to pattern")

    @staticmethod
    def _get_branches(str_branches):
        if not str_branches:
            return []
        branch_pattern = (
            #                                           1      2            3
            r"https://git\.promedweb\.ru/rtmis/" r"(report_(ms|pg))/-/tree/([A-Z]+-\d+)"
        )
        failed_values = []
        branches = []
        for value in split_on_delimiters(str_branches):
            branch = re.match(branch_pattern, value)
            if branch:
                repository_name = branch.group(1)
                branch_name = branch.group(3)
                branches.append(RepositoryBranch(repository_name, branch_name))
            else:
                failed_values.append(value)
        error_message = ""
        if failed_values:
            error_message += (
                f"Branch name values: {failed_values} are not match to pattern"
            )
            raise Exception(error_message)
        if not branches:
            raise Exception("Branches are not found")
        return branches

    @staticmethod
    def _get_templates(str_templates):
        if not str_templates:
            return []
        failed_values = []
        templates = []
        for value in split_on_delimiters(str_templates):
            template = match_template_pattern(value)
            if template:
                templates.append(template)
            else:
                failed_values.append(value)
        if failed_values:
            raise Exception(
                f"Template name values: {failed_values} " f"is not matched to pattern"
            )
        if not templates:
            raise Exception("Templates are not found")
        return templates
