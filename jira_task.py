from logger import *

class JiraTask:
    def __init__(self, name, branches, templates):
        self._name = name
        self._branches = branches
        self._templates = templates
        log_config = load_json(LOG_CONF_FILE_PATH)
        logging.config.dictConfig(log_config)
        self._logger = get_logger(log_config)

    def __str__(self):
        return f"JiraTask {self._name}" \
               f"\nBranches: {', '.join([str(b) for b in self._branches])}" \
               f"\nTemplates: {', '.join([str(t) for t in self._templates])}"

    def __repr__(self):
        return str(self)

    def check_commits(self):
        has_errors = False
        target_branch = load_json(APP_CONF_FILE_PATH)["repository"]["target_branch"]
        changed_templates = []

        for branch in self._branches:
            try:
                changed_templates += branch.get_changed_templates(target_branch)
            except Exception as e:
                has_errors = True
                self._logger.error(e)

        set_of_changed_templates = set(changed_templates)
        set_of_listed_templates = set(self._templates)

        if len(set_of_changed_templates) != len(changed_templates):
            has_errors = True
            self._logger.error("Changed templates contain duplicate")

        if len(set_of_listed_templates) != len(self._templates):
            has_errors = True
            self._logger.error("Self templates contain duplicate")

        if set_difference := set_of_changed_templates - set_of_listed_templates:
            has_errors = True
            self._logger.error(f"Target branch has changes in unlisted files: {', '.join(set_difference)}")

        if set_difference := set_of_listed_templates - set_of_changed_templates:
            has_errors = True
            self._logger.error(f"Listed templates must have changes, but they dont: {', '.join(set_difference)}")

        if has_errors:
            raise Exception("Errors occurs during git repository check")

        return True

    def merge_branches(self):
        target_branch = ""
        for branch in self._branches:
            branch.merge_into(target_branch)