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
            raise Exception("No such RepositoryBranch in REPOSITORIES.")

    def is_contained_in(self, branches):
        pass
        raise Exception("Not implemented")
        # TODO: need to implement method

    def get_changed_templates(self, target_branch):

        try:
            target_commit = self._repo.heads[target_branch].commit
            self_commit = self._repo.heads[self._name].commit
        except Exception as e:
            self._logger.error(str(e))
            raise Exception(f"Repository doesn't contain branches {target_branch} or {self._name}.")
        # a_path может отличаться от b_path наличием папки
        # Вызов match_template_pattern нужен для удаления названия папки из пути файла
        diff_file_names = []

        # TODO: текущее поведение: если в репозитории измененный файл не подходит под шаблон, то бросает исключение
        for diff in target_commit.diff(self_commit):
            name = match_template_pattern(diff.a_path)
            if not name:
                raise Exception(
                    "File name from git repository doesn't match template pattern."
                )
            diff_file_names.append(name)

        return diff_file_names

    def merge_into(self, target_branch):
        try:
            checkout_res = self._repo.git.checkout(target_branch)
            merge_res = self._repo.git.merge(self._name)
            self._logger.info('. '.join(merge_res.split('\n')))
        except Exception as e:
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
