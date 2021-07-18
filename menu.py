from typing import Dict

from jira_api import *
from jira_task import JiraTask
from repo_branch import RepositoryBranch
from taskcreator import TaskCreator
from logger import *
from pathlib import Path
from git import Repo


def fetch_remotes(repositories: Dict[str, Repo]):
    """Обновить локальные копии удаленных веток."""
    has_errors = False
    for repo in repositories.values():
        try:
            repo.git.fetch("--all")
        except Exception as ex:
            logger.error(str(ex))
            has_errors = True
    if has_errors:
        raise Exception(f"Repository fetch failed.")


def save_from_server(version: str) -> str:
    """Сохранить данные с сервера и вернуть имя нового файла."""
    jira_conf = app_conf["jira_conf"]
    jira_conf["versions"] = version
    file_name = pack_data_to_csv(version, CSV_DIR, get_data_dicts(jira_conf))
    return file_name


def read_from_file(file_name: str, repositories: Dict[str, Repo]):
    """Получить список задач. В процессе выполняется проверка регулярными выражениями."""
    data_list = read_from_csv(os.path.join(CSV_DIR, file_name), skip_headers=True)
    return TaskCreator(repositories, app_conf["repository"]["remote"]).create_tasks(data_list)


def check_files(tasks, target_branch, print_details: bool = False):
    """Проверить и сравнить файлы задачи и файлы из гита."""
    if print_details:
        print(f"{'Task':>15} | Status")
    has_errors = False
    for task in tasks:
        verified = False
        try:
            task.check_changed_files(target_branch)
            verified = True
        except Exception as er:
            has_errors = True
            logger.error(str(er))
        if print_details:
            print(f"{task.name:>15} | {('PASS' if verified else 'FAIL')}")
    if has_errors:
        raise Exception(f"Tasks didn't pass files check.")


def merge_tasks(tasks: List[JiraTask], target_branch, print_details: bool = False):
    """Провести слияние веток задач в репозитории."""
    if print_details:
        print(f"{'Task':>15} | Status")
    has_errors = False
    for task in tasks:
        verified = False
        try:
            merge_task_branches(task, target_branch)
            verified = True
        except Exception as ex:
            has_errors = True
            logger.error(str(ex))
        if print_details:
            print(f"{task.name:>15} | {('PASS' if verified else 'FAIL')}")
    if has_errors:
        raise Exception("Error occurred while merging given jira tasks.")


def merge_task_branches(task: JiraTask, target_branch):
    """Провести слияние веток задачи."""
    has_errors = False
    for branch in task.branches:
        try:
            merge_branch(branch, target_branch)
        except Exception as ex:
            has_errors = True
            logger.error(str(ex))
    if has_errors:
        raise Exception(f"Error occurred while processing task {task.name}.")


def merge_branch(branch: RepositoryBranch, target_branch: str):
    """Слить ветку в target_branch."""
    repo = branch.repo
    merge_failed = False
    try:
        checkout_res = repo.git.checkout(target_branch)
        merge_res = repo.git.merge(branch.name)
        logger.info(". ".join(merge_res.split("\n")))
    except Exception as ex:
        merge_failed = True
        logger.error(". ".join(str(ex).split("\n")))
    if merge_failed:
        repo.git.merge("--abort")
        logger.info(f"Merge aborted.")
        raise Exception(
            f"Error occurred while merging branch {branch} to {target_branch}."
        )


def menu_pack_new_data():
    try:
        version = input("Введите версию:")
        file_name = save_from_server(version)
        print(f"Создан новый файл: {file_name}")
    except JIRAError as e:
        logger.error(e)
        print("Произошла ошибка при сохранении данных с сервера Jira.")

    return False


def menu_get_files(directory) -> List[str]:
    """Список файлов в папке. Отсортирован по дате изменения."""
    return [
        file.name
        for file in sorted(
            Path(directory).iterdir(), key=os.path.getmtime, reverse=True
        )
    ]


def menu_show_last_files():
    if files := menu_get_files(CSV_DIR):
        print(f"Последние измененные файлы в папке {CSV_DIR}:")
        for file in files[:5]:
            print(file)
    else:
        print(f"Папка {CSV_DIR} не содержит файлов.")


def menu_user_choice(msg: str, choices: list):
    print(f"Возможный ввод: {choices}")
    while (choice := input(msg)) not in choices:
        print("Повторите ввод.")
    print()
    return choice


def menu_fetch_remotes():
    try:
        fetch_remotes(REPOSITORIES)
        print("Репозитории обновлены.")
    except Exception as ex:
        logger.error(str(ex))
        print("Во вермя обновления репозиториев произошли ошибки.")

    return False


def menu_check_patterns():
    menu_show_last_files()

    file = input(f"\nВведите имя файла в папке {CSV_DIR}('n' - вернуться назад): ")
    if file == "n":
        return

    try:
        read_from_file(file, REPOSITORIES)
        logger.info(f"File {file} passed regex-pattern check.")
        print(f"Файл {file} прошел проверку регулярными выражениями.")
    except Exception as e:
        logger.error(str(e))
        print("Во время проверки паттернов возникли ошибки. Проверьте лог.")

    return False


def menu_check_git():
    menu_show_last_files()

    file = input(f"\nВведите имя файла в папке {CSV_DIR}('n' - вернуться назад): ")
    if file == "n":
        return

    tasks = read_from_file(file, REPOSITORIES)
    try:
        check_files(tasks, TARGET_BRANCH, print_details=True)
        logger.info(f"File {file} passed repository check.")
        print(f"Файл {file} прошел проверку с репозиторием.")
    except Exception as e:
        logger.error(str(e))
        print("Во время проверки репозитория возникли ошибки. Проверьте лог.")

    return False


def menu_merge():
    menu_show_last_files()

    file = input(f"\nВведите имя файла в папке {CSV_DIR}('n' - вернуться назад): ")
    if file == "n":
        return

    tasks = read_from_file(file, REPOSITORIES)
    try:
        merge_tasks(tasks, TARGET_BRANCH, print_details=True)
        logger.info(f"File {file} passed merging.")
        print(f"Файл {file} прошел слияние с репозиторием.")
    except Exception as e:
        logger.error(str(e))
        print("Во время слиния с репозиторием возникли ошибки. Проверьте лог.")

    return False


def start_menu():
    menu_items = {
        "0": {"item": "0. Обновить репозиторий.", "action": menu_fetch_remotes},
        "1": {
            "item": "1. Сохранить данные с сервера Jira в csv файл.",
            "action": menu_pack_new_data,
        },
        "2": {
            "item": "2. Прочитать и проверить данные из файла.",
            "action": menu_check_patterns,
        },
        "3": {"item": "3. Проверить с git.", "action": menu_check_git},
        "4": {"item": "4. Слить ветки.", "action": menu_merge},
        "5": {"item": "5. Выход из программы.", "action": lambda: True},
    }

    exit_program = False
    menu_keys = list(menu_items.keys())

    while not exit_program:
        print("\nМеню:")
        for item in menu_items.values():
            print(item["item"])
        choice = menu_user_choice("Ваш выбор: ", menu_keys)
        exit_program = menu_items[choice]["action"]()

    print("Заврешение работы программы.")


log_config = load_json(LOG_CONF_FILE_PATH)
check_log_folder(log_config)
logging.config.dictConfig(log_config)
logger = get_logger(log_config)
logger.info(f"{'Start app':-^30}")

app_conf = load_json(APP_CONF_FILE_PATH)
CSV_DIR = app_conf["csv_dir"]
create_folder(CSV_DIR)

repo_conf = load_json(APP_CONF_FILE_PATH)["repository"]
REPOSITORIES = {
    "report_ms": Repo(repo_conf["report_ms"]),
    "report_pg": Repo(repo_conf["report_pg"]),
}

TARGET_BRANCH = load_json("app_conf.json")["repository"]["target_branch"]

# try:
#     print("lol")
#     start_menu()
#
# except Exception as e:
#     logger.error(str(e))
#
# logger.info(f"{'Stop app':-^30}")

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
