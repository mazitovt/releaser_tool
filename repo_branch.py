from logger import load_json, APP_CONF_FILE_PATH
from git import Repo, Git
from regex_patterns import match_template_pattern


class RepositoryBranch:
    def __init__(self, repository_name, branch_name):
        self._name = branch_name
        self._repository_name = repository_name
        self._logger = None

    def __str__(self):
        return f"{self._name} in {self._repository_name}"

    def __repr__(self):
        return str(self)

    def is_contained_in(self, branches):
        pass
        raise Exception("Not implemented")
        # TODO: need to implement method

    def get_changed_templates(self, target_branch):

        try:
            repo_path = load_json(APP_CONF_FILE_PATH)["repository"][self._repository_name]
        except Exception as e:
            self._logger.error("No such repository_name in app_conf")
            raise Exception("Error occurred during parsing app_conf")

        repo = Repo(repo_path)
        target_commit = repo.heads[target_branch].commit
        self_commit = repo.heads[self._name].commit

        # a_path может отличаться от b_path наличием папки
        # Вызов match_template_pattern нужен для удаления названия папки из пути файла
        diff_file_names = []

        for diff in target_commit.diff(self_commit):
            name = match_template_pattern(diff.a_path)
            if not name:
                raise Exception(
                    "File name from git repository doesn't match template re-pattern"
                )
            diff_file_names.append(name)

        return diff_file_names

    def merge_into(self, target_branch):
        try:
            repo_path = load_json(APP_CONF_FILE_PATH)["repository"][self._repository_name]
        except Exception as e:
            self._logger.error("No such repository_name in app_conf")
            raise Exception("Error occurred during parsing app_conf")
        try:
            g = Git(repo_path)
            checkout_res = g.checkout(target_branch)
            merge_res = g.merge(self._name)
            self._logger.info(merge_res)
        except Exception as e:
            self._logger.error(e)
            raise Exception("Error occurred during merge process")


        #TODO: Код ниже требует доработки

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
