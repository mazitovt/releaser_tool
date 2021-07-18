import logging
import logging.config

from typing import List, Dict

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
    """Класс для парсинга сырых данных и создания объектов JiraTask"""

    def __init__(self, repositories, remote):
        log_config = load_json(LOG_CONF_FILE_PATH)
        logging.config.dictConfig(log_config)
        self._logger = get_logger(log_config)
        self._repositories = repositories
        self._remote = remote

    def create_tasks(self, tasks_data: List[dict]) -> List[JiraTask]:
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

    def _create_task(self, task_dict: Dict[str, str]) -> JiraTask:
        values_dict = self._try_to_parse_values(task_dict)
        return JiraTask(**values_dict)

    def _try_to_parse_values(self, data_dict: Dict) -> Dict:
        """Проверяет, парсит сырые строки и возвращает словарь с данными."""
        is_successful_parse = True
        values_dict = {"name": None, "branches": [], "templates": []}

        try:
            values_dict["name"] = TaskCreator._get_task_name(data_dict["name"])
        except Exception as e:
            self._logger.error(e)
            is_successful_parse = False

        try:
            values_dict["branches"] = TaskCreator._get_branches(
                data_dict["branches"], self._repositories, self._remote
            )
        except Exception as e:
            self._logger.error(e)
            is_successful_parse = False

        try:
            values_dict["templates"] = TaskCreator._get_templates(
                data_dict["templates"]
            )
        except Exception as e:
            self._logger.error(e)
            is_successful_parse = False

        if not is_successful_parse:
            raise Exception(
                "Values parsing has failed. "
                + (
                    f"See task {values_dict['name']} for more."
                    if values_dict["name"] is not None
                    else ""
                )
            )

        return values_dict

    @staticmethod
    def _get_task_name(value: str) -> str:
        if not value:
            raise Exception("Task name is empty.")
        if task_name := match_task_name_pattern(value):
            return task_name
        raise Exception(f"Task name '{value}' isn't matched to the pattern.")

    @staticmethod
    def _get_branches(
        str_branches: List[str], repositories: Dict[str, RepositoryBranch], remote: str
    ) -> List[RepositoryBranch]:
        failed_values = []
        branches = []
        for value in split_on_delimiters(str_branches):
            if match_args := match_branch_pattern(value):
                match_args["repo"] = repositories[match_args["repository_name"]]
                match_args["branch_name"] = remote + "/" +  match_args["branch_name"]
                branches.append(RepositoryBranch(**match_args))
            else:
                failed_values.append(value)
        if failed_values:
            raise Exception(
                f"Branch name values aren't matched to the pattern: {failed_values}."
            )
        if not branches:
            raise Exception("Branches are not found.")
        return branches

    @staticmethod
    def _get_templates(str_templates: str) -> List[str]:
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
