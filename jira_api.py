import json
import os
from datetime import datetime as dt
from typing import List

from jira import JIRA
from jira.exceptions import JIRAError

from csv import DictWriter, DictReader


def load_json(json_file_path):
    with open(json_file_path, "r") as conf_file:
        return json.load(conf_file)


def create_folder(directory):
    """
    Проверяет существование каталога для сохранения логов,
    если задано логгирование в файл.
    Создает каталог если он не существует.
    """
    if not os.path.isdir(directory):
        os.mkdir(directory)


def read_from_csv(file_path, skip_headers: bool) -> List[dict]:
    """
    Чтение файла из папки.
    :param skip_headers: пропускать ли первую строку
    :param file_path: путь к файлу из текущей директории
    :return: список словарей
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
    with open(file_path, mode="r") as file:
        reader = DictReader(f=file, fieldnames=["name", "branches", "templates"])
        if skip_headers:
            next(reader)
        return [item for item in reader]


def pack_data_to_csv(csv_dir, list_of_data_dict) -> str:
    """
    Упаковка данных в csv файл

    :param csv_dir: название существующей папки, куда будет сохранен файл
    :param list_of_data_dict: список словарей
    :return: имя файла
    """
    while os.path.exists(
            csv_name := "jira_export_" + dt.now().strftime("%Y-%m-%dT%H_%M_%S") + ".csv"
    ):
        pass

    with open(os.path.join(csv_dir, csv_name), "w+", newline="") as file:
        # Ошибка, если пустой список data_list_of_dict
        # writer = DictWriter(f=file, fieldnames=data_list_of_dict[0].keys())
        writer = DictWriter(f=file, fieldnames=["name", "branches", "templates"])
        writer.writeheader()
        writer.writerows(list_of_data_dict)

    return csv_name


def jira_issues(server, user_login, password, jql, max_result=100, proxy = None):
    """
    Возвращает список задач по jql запросу

    :param user_login: логин
    :param password: пароль
    :param jql: JQL запрос
    :param server: адрес сервера
    :param max_result: максимальное количество задач
    :param proxy: адрес прокси сервера
    :return: список словарей
    """
    try:
        if proxy:
            os.environ['https_proxy'] = os.environ['http_proxy'] = proxy
        jira_connection = JIRA(server=server, basic_auth=(user_login, password))
    except JIRAError as e:
        raise JIRAError("Error occurred while trying to connect to jira server." + str(e))
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
    :return: список словарей
    """
    jql_query = f"project in ({jira_conf['projects']}) AND " \
                f"status in ({jira_conf['status']}) " \
                f"AND fixVersion in ({jira_conf['versions']}) " \
                f"AND component in (Отчеты, \"Печатные формы\") "

    return jira_issues(
        server=jira_conf["server"],
        user_login=jira_conf["login"],
        password=jira_conf["password"],
        max_result=jira_conf["maxResult"],
        proxy=jira_conf["proxy"],
        jql=jql_query
    )


