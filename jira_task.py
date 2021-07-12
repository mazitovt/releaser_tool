from logger import *

TARGET_BRANCH = load_json("app_conf.json")["repository"]["target_branch"]

class JiraTask:
    """
    Задача из Jira
    """

    def __init__(self, name, branches, templates):
        self._name = name
        self._branches = branches
        self._templates = templates
        log_config = load_json(LOG_CONF_FILE_PATH)
        logging.config.dictConfig(log_config)
        self._logger = get_logger(log_config)

    def __str__(self):
        return (
            f"Task: {self._name}"
            + "\nBranches: " + ("\n" + 10 * " ").join([str(b) for b in self._branches])
            + "\nTemplates: " + ("\n" + 11 * " ").join([str(t) for t in self._templates])
        )

    def __repr__(self):
        return str(self)

    def check_commits(self):
        has_errors = False
        changed_templates = []

        for branch in self._branches:
            try:
                changed_templates += branch.get_changed_templates(TARGET_BRANCH)
            except Exception as e:
                has_errors = True
                self._logger.error(str(e))

        set_of_changed_templates = set(changed_templates)
        set_of_self_templates = set(self._templates)

        # if len(set_of_changed_templates) != len(changed_templates):
        #     has_errors = True
        #     self._logger.error("Changed templates contain duplicate")
        #
        # if len(set_of_self_templates) != len(self._templates):
        #     has_errors = True
        #     self._logger.error("Self templates contain duplicate")

        if set_difference := set_of_changed_templates - set_of_self_templates:
            has_errors = True
            self._logger.error(
                f"Target branch has changes in unlisted files: {', '.join(set_difference)}."
            )

        if set_difference := set_of_self_templates - set_of_changed_templates:
            has_errors = True
            self._logger.error(
                f"Listed templates must have changes, but they don't: {', '.join(set_difference)}."
            )

        if has_errors:
            raise Exception(f"Errors occurs during git repository check. See task {self._name} for more.")

        return True

    def merge_branches(self):
        for branch in self._branches:
            branch.merge_into(TARGET_BRANCH)
