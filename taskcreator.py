import logging
import logging.config


class TaskCreator:
    def __init__(self, all_branches, config_dict):
        logging.config.dictConfig(config_dict)
        self._logger = logging.getLogger(__name__)
        self._branches = all_branches

    def create_tasks_from_list(self, tasks_data):
        jira_tasks = []
        error_row_count = 0
        for row in tasks_data:
            if _is_row_checked(row):
                jira_tasks.append(self._create_task(row))
            else:
                error_row_count += 1
        if error_row_count == 0:
            return jira_tasks
        raise Exception("Tasks has errors")

    def _is_row_checked(self, row):
        is_checked = True
        try:
            self._check_branches(row)
        except Exception as ex:
            self._logger.exception(ex)
            is_checked = False
        try:
            self._check_templates(row)
        except Exception as ex:
            self._logger.exception(ex)
            is_checked = False
        return is_checked

    def _create_task(self, row):
        pass

    def _check_branches(self, row):
        pass

    def _check_templates(self, row):
        pass