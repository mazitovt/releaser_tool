from logger import *
from git import Repo


class RepositoryBranch:
    def __init__(self, repository_name, branch_name):
        self._name = branch_name
        self._repository_name = repository_name
        # log_config = load_json(LOG_CONF_FILE_PATH)
        # logging.config.dictConfig(log_config)
        # self._logger = get_logger(log_config)

    def __str__(self):
        return f"{self._name} in {self._repository_name}"

    def __repr__(self):
        return str(self)

    def is_contained_in(self, branches):
        pass
        raise Exception("Not implemented")
        # TODO: need to implement method

    def get_changed_templates(self, target_branch):
        repo_path = load_json(APP_CONF_FILE_PATH)["repository"][self._repository_name]
        repo = Repo(repo_path)

        target_commit = repo.heads[target_branch].commit
        self_commit = repo.heads[self._name].commit

        # a_path может отличаться от b_path наличием папки
        # Вызов match_template_pattern нужен для удаления названия папки из пути файла
        # return [TaskCreator.match_template_pattern(diff.a_path) for diff in target_commit.diff(self_commit)]

        diff_file_names = []

        # for diff in target_commit.diff(self_commit):
        #     name = TaskCreator.match_template_pattern(diff.a_path)
        #     if not name:
        #         raise Exception("File name from git repository doesn't match template re-pattern")
        #     diff_file_names.append(name)

        return diff_file_names

    def merge_into(self, target_branch):
        pass
        raise Exception("Not implemented")
        # TODO: need to implement method
