import logging
from jira.exceptions import JIRAError
from jira_api import *
from taskcreator import TaskCreator
from logger import *


def print_raw_data(data_list_of_dict):
    """
    Печать сырых данных(название задачи, ветки, шаблоны) с сервера
    :param data_list_of_dict: список словарей
    :return: None
    """
    print("{'Start of raw data':-^30}")
    for i in data_list_of_dict:
        print()
        for k, v in i.items():
            print(f"{k}: {v}")
    print("{'End of raw data':-^30}")


def pack_new_data():
    try:
        jira_conf = app_conf["jira_conf"]
        file_name = pack_data_to_csv(CSV_DIR, get_data_dicts(jira_conf))
        print(f"Создан новый файл: {os.path.join(CSV_DIR, file_name)}")
    except JIRAError as e:
        logger.error(e)
        print("Произошла ошибка при сохранении данных с сервера Jira.")

    return False


def get_tasks_list(file):
    list_of_data_dicts = read_from_csv(os.path.join(CSV_DIR, file), skip_headers=True)
    logger.info(f"Working with {file}.")
    return TaskCreator().create_tasks(list_of_data_dicts)


def check_patterns():
    try:
        show_last_files()

        file = input(f"\nВведите имя файла в папке {CSV_DIR}('n' - вернуться назад): ")
        if file == "n":
            return

        get_tasks_list(file)

        logger.info(f"File {file} passed regex-pattern check.")
        print(f"Файл {file} прошел проверку регулярными выражениями.")
    except Exception as e:
        logger.error(str(e))
        print("Во время проверки паттернов возникли ошибки. Проверьте лог.")

    return False


def check_git():
    has_no_errors = True

    try:
        show_last_files()

        file = input(f"\nВведите имя файла в папке {CSV_DIR}('n' - вернуться назад): ")
        if file == "n":
            return

        print(' '*9 + "Задача | Статус проверки")
        for task in get_tasks_list(file):
            verified = False
            try:
                # print(f"Проверяю задачу {task._name}", end="\r")
                task.check_commits()
                verified = True
            except Exception as e:
                has_no_errors = False
                logger.error(str(e))

            print(f"{task._name} | {('PASS' if verified else 'FAIL')}")

        if has_no_errors:
            logger.info(f"File {file} passed git check.")
            print(f"Файл {file} прошел проверку с git репозиторием.")
        else:
            raise Exception(f"File {file} didn't pass git check.")
    except Exception as e:
        logger.error(str(e))
        print("Во время проверки репозитория возникли ошибки. Проверьте лог.")

    return False


def merge_branches():

    has_no_errors = True

    try:
        show_last_files()

        file = input(f"\nВведите имя файла в папке {CSV_DIR}('n' - вернуться назад): ")
        if file == "n":
            return

        print(' ' * 9 + "Задача | Статус слияния")
        for task in get_tasks_list(file):
            verified = False
            try:
                # print(f"Проверяю задачу {task._name}", end="\r")
                task.merge_branches()
                verified = True
            except Exception as e:
                has_no_errors = False
                logger.error(str(e))

            print(f"{task._name} | {('PASS' if verified else 'FAIL')}")

        if has_no_errors:
            logger.info(f"File {file} passed git merge.")
            print(f"Файл {file} прошел слияние с репозиторием.")
        else:
            raise Exception(f"File {file} didn't pass git merge.")
    except Exception as e:
        logger.error(str(e))
        print("Во время слиния с репозиторием возникли ошибки. Проверьте лог.")

    return False


def get_last_updated_files_list(dir):
    return [
        file.name
        for file in sorted(Path(dir).iterdir(), key=os.path.getmtime, reverse=True)
    ]


def show_last_files():
    files = get_last_updated_files_list(CSV_DIR)

    if files:
        print(f"Последние измененные файлы в папке {CSV_DIR}:")
        index = 0
        while index < 5 and index < len(files):
            print(files[index])
            index += 1
    else:
        print(f"Папка {CSV_DIR} не содержит файлов.")


def user_choice(msg: str, choices: list):
    print(f"Возможный ввод: {choices}")
    while (choice := input(msg)) not in choices:
        print("Повторите ввод.")
    print()
    return choice


def menu():
    menu_items = {
        "1": {
            "item": "1. Сохранить данные с сервера Jira в csv файл.",
            "action": pack_new_data,
        },
        "2": {
            "item": "2. Прочитать и проверить данные из файла.",
            "action": check_patterns,
        },
        "3": {"item": "3. Проверить с git.", "action": check_git},
        "4": {"item": "4. Слить ветки.", "action": merge_branches},
        "5": {"item": "5. Выход из программы.", "action": lambda: True},
    }

    exit_program = False
    menu_keys = list(menu_items.keys())

    while not exit_program:
        print("\nМеню:")
        for item in menu_items.values():
            print(item["item"])
        choice = user_choice("Ваш выбор: ", menu_keys)
        exit_program = menu_items[choice]["action"]()

    print("Заврешение работы программы.")


log_config = load_json(LOG_CONF_FILE_PATH)
check_log_folder(log_config)
logging.config.dictConfig(log_config)
logger = get_logger(log_config)
logger.info(f"{'Start app':-^30}")

app_conf = load_json(APP_CONF_FILE_PATH)
CSV_DIR = app_conf["csv_dir"]
menu()

logger.info(f"{'Stop app':-^30}")



#
# app_conf = load_json(APP_CONF_FILE_PATH)
# csv_dir = app_conf["csv_dir"]
#
# pack_new_data(app_conf)
#
# try:
#     file = get_last_updated_file_name(csv_dir)
#     list_of_data_dicts = read_from_csv(os.path.join(csv_dir, file))
#     create_jira_tasks_from_jira_api(list_of_data_dicts)
# except Exception as e:
#     print(e)

# def get_commit_from_range(start_commit, end_commit):
#     repo = git.Repo(xxx)
#     commit_range = "%s...%s" % (start_commit, end_commit)
#     result = repo.iter_commits(commit_range)
#     for commit in result:
#        print(commit.message)


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
