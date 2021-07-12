import logging
import logging.config
from logger import LOG_CONF_FILE_PATH, load_json, get_logger
from jira_task import JiraTask
from repo_branch import RepositoryBranch
from regex_patterns import (
    match_task_name_pattern,
    match_branch_pattern,
    match_template_pattern,
    split_on_delimiters,
)


class TaskCreator:
    def __init__(self):
        log_config = load_json(LOG_CONF_FILE_PATH)
        logging.config.dictConfig(log_config)
        self._logger = get_logger(log_config)
        pass

    def create_tasks(self, tasks_data: list):
        jira_tasks = []
        has_errors = False
        for task_dict in tasks_data:
            try:
                jira_tasks.append(self._create_task(task_dict))
            except Exception as e:
                self._logger.error(e)
                has_errors = True
        if has_errors:
            raise Exception("Input data contains errors.")

        return jira_tasks

    def _create_task(self, task_dict):
        values_dict = TaskCreator._try_to_parse_values(self._logger, task_dict)
        return JiraTask(**values_dict)

    @staticmethod
    def _try_to_parse_values(logger, data_dict):
        """

        :param logger: логгер
        :param data_dict: словарь с полями "name", "branches", "templates".
        :return: словарь с полями "name", "branches", "templates".
        """
        is_successful_parse = True
        values_dict = {"name": None, "branches": [], "templates": []}

        parse_actions = (
            TaskCreator._get_task_name,
            TaskCreator._get_branches,
            TaskCreator._get_templates,
        )

        for field, action in zip(data_dict.keys(), parse_actions):
            try:
                values_dict[field] = action(data_dict[field])
            except Exception as e:
                logger.error(e)
                is_successful_parse = False

        if not is_successful_parse:
            raise Exception(
                "Values parsing has failed. "
                + (
                    f"See task {values_dict['name']} for more."
                    if values_dict['name'] is not None
                    else ""
                )
            )

        return values_dict

    @staticmethod
    def _get_task_name(value):
        if not value:
            raise Exception("Task name is empty.")
        if task_name := match_task_name_pattern(value):
            return task_name
        raise Exception(f"Task name '{value}' isn't matched to the pattern.")

    @staticmethod
    def _get_branches(str_branches):
        failed_values = []
        branches = []
        for value in split_on_delimiters(str_branches):
            if match := match_branch_pattern(value):
                branches.append(RepositoryBranch(**match))
            else:
                failed_values.append(value)
        if failed_values:
            raise Exception(
                f"Branch name values are not match to the pattern: {failed_values}."
            )
        if not branches:
            raise Exception("Branches are not found.")
        return branches

    @staticmethod
    def _get_templates(str_templates):
        failed_values = []
        templates = []
        for value in split_on_delimiters(str_templates):
            if template := match_template_pattern(value):
                templates.append(template)
            else:
                failed_values.append(value)
        if failed_values:
            raise Exception(
                f"Template name values aren't matched to the pattern: {failed_values}."
            )
        if not templates:
            raise Exception("Templates are not found.")
        return templates
