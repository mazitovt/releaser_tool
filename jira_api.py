from jira import JIRA


def jira_issues(
    user_login, password, jql, server="https://jira.is-mis.ru", max_result=100
):
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
    issues = jira_connection.search_issues(maxResults=max_result, jql_str=jql)

    return [
        {
            "id": issue.raw["id"],
            "key": issue.raw["key"],
            "branches": issue.raw["fields"]["customfield_12501"],
            "templates": issue.raw["fields"]["customfield_11983"],
        }
        for issue in issues
    ]
