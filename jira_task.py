from typing import List

from logger import *
from repo_branch import RepositoryBranch


class JiraTask:
    """Задача из Jira."""

    def __init__(self, name: str, branches: List[RepositoryBranch], templates: List[str]):
        self._name = name
        self._branches = branches
        self._templates = templates
        log_config = load_json(LOG_CONF_FILE_PATH)
        logging.config.dictConfig(log_config)
        self._logger = get_logger(log_config)

    @property
    def name(self):
        return self._name

    @property
    def branches(self):
        return self._branches

    def __str__(self):
        return (
                f"Task: {self._name}"
                + "\nBranches: " + ("\n" + 10 * " ").join([str(b) for b in self._branches])
                + "\nTemplates: " + ("\n" + 11 * " ").join([str(t) for t in self._templates])
        )

    def __repr__(self):
        return str(self)

    def check_changed_files(self, target_branch):
        """Сравнение своих шаблонов и измененных файлов в репозитории."""
        has_errors = False
        changed_files = []

        for branch in self._branches:
            try:
                changed_files += branch.diff_self_and_common_commits(target_branch)
            except Exception as e:
                has_errors = True
                self._logger.error(str(e))

        set_of_changed_templates = set(changed_files)
        set_of_self_templates = set(self._templates)

        # TODO: ошибка 1 на задаче 70470, 58513
        # if len(set_of_changed_templates) != len(changed_files):
        #     has_errors = True
        #     self._logger.error("Changed templates contain duplicate.")

        # TODO: ошибка 2 на задаче 70470, 58513
        # if len(set_of_self_templates) != len(self._templates):
        #     has_errors = True
        #     self._logger.error("Self templates contain duplicate.")

        if set_difference := set_of_changed_templates - set_of_self_templates:
            has_errors = True
            self._logger.error(
                f"Branch has changes in unlisted files: {', '.join(set_difference)}."
            )

        if set_difference := set_of_self_templates - set_of_changed_templates:
            has_errors = True
            self._logger.error(
                f"Listed templates must have changes, but they don't: {', '.join(set_difference)}."
            )

        for branch in self._branches:
            # Проверка, что в целевой ветки не изменялись файлы шаблонов из self._templates
            set_of_target_branch_changes = set(branch.diff_target_and_common_commits(target_branch))
            if set_intersection := set_of_target_branch_changes & set_of_self_templates:
                has_errors = True
                self._logger.error(
                    f"Target branch '{target_branch}' contains changes in files, that can't be changed: {', '.join(set_intersection)}.")

        if has_errors:
            raise Exception(f"Errors occurred while git repository check. See task {self._name} for more.")

        return True
