class RepositoryBranch:
    def __init__(self, repository_name, branch_name):
        self._name = branch_name
        self._repository_name = repository_name


class JiraTask:
    def __init__(self, name, branches, templates):
        self._name = name
        self._branches = branches
        self._templates = templates
