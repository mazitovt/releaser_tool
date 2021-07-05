from jira_api import get_data_dict
from taskcreator import TaskCreator
from logger import *


# def get_commit_from_range(start_commit, end_commit):
#     repo = git.Repo(xxx)
#     commit_range = "%s...%s" % (start_commit, end_commit)
#     result = repo.iter_commits(commit_range)
#     for commit in result:
#        print(commit.message)

def print_raw_data(data_list_of_dict):
    """
    Печать сырых данных(название задачи, ветки, шаблоны) с сервера
    :param data_list_of_dict: список словарей
    :return: None
    """
    print(30 * "-" + "Start of raw data" + 30 * "-")
    for i in data_list_of_dict:
        print()
        for k, v in i.items():
            print(f"{k}: {v}")
    print(30 * "-" + "End of raw data" + 30 * "-")


def create_jira_tasks_from_jira_api():
    """
    Демонстарция создания объектов JiraTask из данных с сервера jira
    :return: None
    """
    data_list_of_dict = get_data_dict()

    tc = TaskCreator("")

    print_raw_data(data_list_of_dict)

    # В задаче PROMEDWEB-60174 были добавлены заметки в поле 'Действие при обновлении',
    # что вызывало ошибку в методе _get_branches
    data_list_of_dict = [item for item in data_list_of_dict if item["name"] != "PROMEDWEB-60174"]

    try:
        r = tc.create_tasks_from_list(data_list_of_dict)
        for task in r:
            print(task)
    except Exception as e:
        logger.exception(e)
        print()
        print("Error occurred. Check logs")


log_config = load_json(LOG_CONF_FILE_PATH)
logging.config.dictConfig(log_config)
check_log_folder(log_config)
logger = get_logger(log_config)
logger.info("Start app")
create_jira_tasks_from_jira_api()

# def main():
#     has_errors = False
#     data = get_jira_data()
#     task_creator = TaskCreator(data)
#     tasks = task_creator.get_jira_tasks_list()
#     if len(data) != len(tasks):
#         has_errors = True
#     for task in tasks:
#         if not task.check(target_branch, repo):
#             has_errors = True
#     if not has_errors:
#         for task in tasks:
#             for branch in task.branches:
#                 branch.merge(target_branch, repo)
