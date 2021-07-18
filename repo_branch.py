from typing import List

from logger import load_json, LOG_CONF_FILE_PATH, get_logger
import logging
import logging.config
from git import Repo
import os


class RepositoryBranch:
    """Ветка в git репозитории"""

    def __init__(self, repo: Repo, repository_name: str, branch_name: str):
        self._name = branch_name
        self._repository_name = repository_name
        self._repo = repo
        log_config = load_json(LOG_CONF_FILE_PATH)
        logging.config.dictConfig(log_config)
        self._logger = get_logger(log_config)

    @property
    def name(self):
        return self._name

    @property
    def repo(self):
        return self._repo

    def __str__(self):
        return f"{self._name} in {self._repository_name}"

    def __repr__(self):
        return str(self)

    def diff_self_and_common_commits(self, target_branch):
        """Получить список измененных файлов между своей веткой и общим предком."""
        common_commit = self._get_commit(self._get_common_commit_name(self._name, target_branch))
        self_commit = self._get_commit(self._name)
        return RepositoryBranch._get_changed_files(common_commit, self_commit)

    def diff_target_and_common_commits(self, target_branch):
        """Получить список измененных файлов между целевой веткой и общим предком."""
        common_commit = self._get_commit(self._get_common_commit_name(self._name, target_branch))
        target_commit = self._get_commit(target_branch)
        return RepositoryBranch._get_changed_files(common_commit, target_commit)

    def _get_common_commit_name(self, branch_1, branch_2) -> str:
        """Получить имя ближайшего общего коммита двух веток."""
        try:
            return self._repo.git.merge_base([branch_1, branch_2])
        except Exception as e:
            self._logger.error(str(e))
            raise Exception(f"Error occurred while finding common commit for {branch_1} and {branch_2}.")

    def _get_commit(self, branch):
        """Получить коммит, на который указывает ветка."""
        try:
            return self._repo.commit(branch)
        except Exception as e:
            self._logger.error(str(e))
            raise Exception(f"Repository doesn't contain branch {branch}.")

    @staticmethod
    def _get_changed_files(from_commit, to_commit) -> List[str]:
        return [os.path.basename(diff.a_path) for diff in to_commit.diff(from_commit)]

