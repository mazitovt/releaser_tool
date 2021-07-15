from logger import load_json, APP_CONF_FILE_PATH, LOG_CONF_FILE_PATH, get_logger
import logging
import logging.config
from git import Repo, Git
from regex_patterns import match_template_pattern


class RepositoryBranch:
    """
    Ветка в git репозитории
    """
    # TODO: Ошибка, если не заполенены поля report_ms и report_pg в app.conf
    repo_conf = load_json(APP_CONF_FILE_PATH)["repository"]
    REPOSITORIES = {
        "report_ms": {
            "repo": Repo(repo_conf["report_ms"]),
            "repo_path": repo_conf["report_ms"],
        },
        "report_pg": {
            "repo": Repo(repo_conf["report_pg"]),
            "repo_path": repo_conf["report_pg"],
        },
    }

    def __init__(self, repository_name, branch_name):
        self._name = branch_name
        self._repository_name = repository_name
        self._repo = self._get_repo()
        log_config = load_json(LOG_CONF_FILE_PATH)
        logging.config.dictConfig(log_config)
        self._logger = get_logger(log_config)

    def __str__(self):
        return f"{self._name} in {self._repository_name}"

    def __repr__(self):
        return str(self)

    def _get_repo(self):
        try:
            return RepositoryBranch.REPOSITORIES[self._repository_name]["repo"]
        except Exception as e:
            self._logger.error(str(e))
            raise Exception("No such RepositoryBranch in REPOSITORIES.")

    def is_contained_in(self, branches):
        pass
        raise Exception("Not implemented")
        # TODO: need to implement method

    def get_target_branch_changes(self, to_branch):
        """
        Получить список файлов, у которых есть разница между целевой веткой или ближайшим предком своей и целевой веток.
        :param target_branch:
        :return:
        """
        from_commit = self.get_common_commit(to_branch)
        to_commit = self.get_commit(to_branch)
        return RepositoryBranch.get_changed_files(from_commit, to_commit)

    def get_changed_templates(self, to_branch):
        """
        Получить список файлов, у которых есть разница между своей веткой или ближайшим предком своей и целевой веток.
        :param target_branch:
        :return:
        """
        from_commit = self.get_commit(self._name)
        to_commit = self.get_common_commit(to_branch)
        return RepositoryBranch.s_get_changed_templates(from_commit, to_commit)

    def get_common_commit(self, to_branch):
        common_commit_name = self._repo.git.merge_base([self._name, to_branch])
        return self.get_commit(common_commit_name)

    def get_commit(self, branch):
        try:
            return self._repo.commit(branch)
        except Exception as e:
            self._logger.error(str(e))
            raise Exception(f"Repository doesn't contain branch {branch}.")

    def merge_into(self, target_branch):
        """
        Слить ветку в target_branch.
        :param target_branch:
        :return:
        """

        merge_failed = False
        try:
            checkout_res = self._repo.git.checkout(target_branch)
            merge_res = self._repo.git.merge(self._name)
            self._logger.info('. '.join(merge_res.split('\n')))
        except Exception as e:
            merge_failed = True
            self._logger.error('. '.join(str(e).split('\n')))
        if merge_failed:
            res = self._repo.git.merge("--abort")
            self._logger.info(f"Merge aborted.")
            raise Exception("Error occurred while merging.")

        # TODO: Код ниже (требует доработки) - альтернатива self._repo.git.merge(self._name)

        # repo_path = load_json(APP_CONF_FILE_PATH)["repository"][self._repository_name]
        # repo = Repo(repo_path)
        #
        # target_branch = repo.heads[target_branch]
        # self_branch = repo.heads[self._name]
        #
        # target_branch.checkout()
        #
        # merge_base = repo.merge_base(self_branch, target_branch)
        #
        # repo.index.merge_tree(target_branch, base = merge_base)
        #
        # repo.index.commit("Merge self_branch into target_branch", parent_commits=(self_branch.commit, target_branch.commit))
        #
        # self_branch.checkout(force = True)
        #
        # # target_branch.commit = self_branch.commit

    @staticmethod
    def s_get_changed_templates(from_commit, to_commit):

        # a_path может отличаться от b_path наличием папки
        # Вызов match_template_pattern нужен для удаления названия папки из пути файла
        diff_file_names = []

        # TODO: текущее поведение: если в репозитории измененный файл не подходит под шаблон, то бросает исключение
        for diff in to_commit.diff(from_commit):
            name = match_template_pattern(diff.a_path)
            if not name:
                raise Exception(
                    f"File name {diff.a_path} from git repository doesn't match template pattern."
                )
            diff_file_names.append(name)

        return diff_file_names

    @staticmethod
    def get_changed_files(from_commit, to_commit):
        return [diff.a_path for diff in to_commit.diff(from_commit)]
