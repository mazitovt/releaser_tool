import json
import os
from typing import List

from jira import JIRA
from jira.exceptions import JIRAError

from csv import DictWriter, DictReader


def load_json(json_file_path):
    """Прочиатать json файл."""
    with open(json_file_path, "r") as conf_file:
        return json.load(conf_file)


def create_folder(directory):
    """
    Создает каталог, если он не существует.
    """
    if not os.path.isdir(directory):
        os.mkdir(directory)


def read_from_csv(file_path, skip_headers: bool) -> List[dict]:
    """
    Чтение файла из папки.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
    with open(file_path, mode="r") as file:
        reader = DictReader(f=file, fieldnames=["name", "branches", "templates"])
        if skip_headers:
            next(reader)
        return [item for item in reader]


def pack_data_to_csv(file_name, csv_dir, list_of_data_dict) -> str:
    """
    Упаковка данных в csv файл. Перезаписывает, если существует.
    """
    i = 0
    while os.path.exists(
        csv_path := os.path.join(
            csv_dir, file_name + f"{(('_' + str(i)) if i else '')}" + ".csv"
        )
    ):
        i += 1

    with open(csv_path, "w+", newline="") as file:
        writer = DictWriter(f=file, fieldnames=["name", "branches", "templates"])
        writer.writeheader()
        writer.writerows(list_of_data_dict)

    return csv_path


def jira_issues(server, user_login, password, jql, max_result=100, proxy=None):
    """
    Возвращает список задач по jql запросу
    """
    try:
        if proxy:
            os.environ["https_proxy"] = os.environ["http_proxy"] = proxy
        jira_connection = JIRA(server=server, basic_auth=(user_login, password))
    except JIRAError as e:
        raise JIRAError(
            "Error occurred while trying to connect to jira server." + str(e)
        )

    # 'key' - имя задачи (PROMEDWEB-XXXXX)
    # 'customfield_11983' - поле 'Действие при обновлении'
    # 'customfield_12501' - поле 'Шаблоны отчетов'
    issues = jira_connection.search_issues(
        maxResults=max_result,
        jql_str=jql,
        fields=["key", "customfield_11983", "customfield_12501"],
    )

    return [
        {
            "name": issue.key,
            "branches": issue.fields.customfield_11983,
            "templates": issue.fields.customfield_12501,
        }
        for issue in issues
    ]


def get_data_dicts(jira_conf: dict) -> List[dict]:
    """
    Получить список задач с серверов Jira
    """

    jql_query = (
        f"fixVersion in ({jira_conf['versions']}) "
        f'AND component in (Отчеты, "Печатные формы") '
    )

    return jira_issues(
        server=jira_conf["server"],
        user_login=jira_conf["login"],
        password=jira_conf["password"],
        max_result=jira_conf["maxResult"],
        proxy=jira_conf["proxy"],
        jql=jql_query,
    )
