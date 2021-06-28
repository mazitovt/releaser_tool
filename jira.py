class RepositoryBranch:
    def __init__(self, repository_name, branch_name):
        self._name = branch_name
        self._repository_name = repository_name

    def is_contained_in(self, branches):
        pass
        raise Exception("Not implemented")
        # TODO: need to implement method

    def get_changed_templates(self, target_branch):
        pass
        raise Exception("Not implemented")
        # TODO: need to implement method

    def merge_into(self, target_branch):
        pass
        raise Exception("Not implemented")
        # TODO: need to implement method


class JiraTask:
    def __init__(self, name, branches, templates):
        self._name = name
        self._branches = branches
        self._templates = templates

    def check_commits(self):
        changed_templates = []
        for branch in self._branches:
            changed_templates = branch.get_changed_templates(target_branch)
        for template in changed_templates:
            if template not in self._templates:
                raise Exception("Not implemented")
        self._check_templates_vise_versa()

    def merge_branches(self):
        for branch in self._branches:
            branch.merge_into(target_branch)

    def _check_templates_vise_versa(self):
        pass
