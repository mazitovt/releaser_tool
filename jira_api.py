from jira import JIRA
import json

APP_CONF_FILE_PATH = "app_conf.json"


def load_json(json_file_path):
    with open(json_file_path, "r") as conf_file:
        return json.load(conf_file)


def jira_issues(server, user_login, password, jql, max_result=100):
    """
    Возвращает список задач по запросу

    :param user_login: логин
    :param password: пароль
    :param jql: JQL запрос
    :param server: адрес сервера
    :param max_result: максимальное количество задач
    :return: список словарей
    """
    jira_connection = JIRA(server=server, basic_auth=(user_login, password))

    # key - имя задачи (PROMEDWEB-XXXXX)
    # 'customfield_11983' - поле 'Действие при обновлении'
    # 'customfield_12501' - поле 'Шаблоны отчетов'
    issues = jira_connection.search_issues(maxResults=max_result, jql_str=jql, fields=['key','customfield_11983', 'customfield_12501'])

    return [
        {
            "name": issue.key,
            "branches": issue.fields.customfield_11983,
            "templates": issue.fields.customfield_12501,
        }
        for issue in issues
    ]

    # return [
    #     {
    #         # "id": issue.raw["id"],
    #         "name": issue.raw["key"],
    #         "branches": issue.raw["fields"]["customfield_12501"],
    #         "templates": issue.raw["fields"]["customfield_11983"],
    #     }
    #     for issue in issues
    # ]


def get_data_dict():
    """
    Получить список задач с серверов Jira с помощь app_conf.json

    :return: список словарей
    """
    app_conf = load_json(APP_CONF_FILE_PATH)
    jira_conf = app_conf["jira_api"]

    jql_query = f"project in ({jira_conf['projects']}) AND status in ({jira_conf['status']}) AND fixVersion in ({jira_conf['versions']}) AND component in (Отчеты, \"Печатные формы\")"

    return jira_issues(
        server=jira_conf["server"],
        user_login=jira_conf["login"],
        password=jira_conf["password"],
        max_result=jira_conf["maxResult"],
        jql=jql_query,
    )


def get_data_list():
    """
    Получить список задач с серверов Jira с помощь app_conf.json

    :return: список списков строк
    """
    app_conf = load_json(APP_CONF_FILE_PATH)
    jira_conf = app_conf["jira_api"]

    jql_query = f"project in ({jira_conf['projects']}) AND status in ({jira_conf['status']}) AND fixVersion in ({jira_conf['versions']}) AND component in (Отчеты, \"Печатные формы\")"

    issues = jira_issues(
        server=jira_conf["server"],
        user_login=jira_conf["login"],
        password=jira_conf["password"],
        max_result=jira_conf["maxResult"],
        jql=jql_query,
    )

    return [list(issue.values()) for issue in issues]
#
# for i in get_data_dict():
#     for k,v in i.items():
#         print(k,v)
# for i in get_data_list():
#     print(i)