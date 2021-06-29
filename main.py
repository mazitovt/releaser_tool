from jira_api import get_data_dict
from taskcreator import TaskCreator
from logger import *

def main():
    log_config = load_json(LOG_CONF_FILE_PATH)
    logging.config.dictConfig(log_config)
    check_log_folder(log_config)
    logger = get_logger(log_config)
    logger.info('Start app')

    data_list_of_dict = get_data_dict()

    tc = TaskCreator("", log_config)

    for i in data_list_of_dict:
        for k, v in i.items():
            print(k,v)

    try:
        r = tc.create_tasks_from_list(data_list_of_dict)
        for task in r:
            print(task)
    except Exception as e:
        logger.exception(e)
        print('Error occurred. Check logs')

main()


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


