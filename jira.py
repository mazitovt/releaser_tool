import logging.config

column_names = [
    "Ключ проблемы",
    "Идентификатор проблемы",
    "Тип задачи",
    "Статус",
    "Тема",
    "Исправить в версиях",
    "Действия при обновлении",
    "Ссылка на yml",
    "Ветка в Git",
    "Шаблоны отчетов",
    "Шаблоны MS",
    "Шаблоны PG",
    "Объекты в БД",
    "Объекты в MS",
    "Объекты в PG",
]

column_index_to_name = {
    0: "Ключ проблемы",
    1: "Идентификатор проблемы",
    2: "Тип задачи",
    3: "Статус",
    4: "Тема",
    5: "Исправить в версиях",
    6: "Действия при обновлении",
    7: "Ссылка на yml",
    8: "Ветка в Git",
    9: "Шаблоны отчетов",
    10: "Шаблоны MS",
    11: "Шаблоны PG",
    12: "Объекты в БД",
    13: "Объекты в MS",
    14: "Объекты в PG",
}


def better_split_params(params, one_or_none):
    """
    Разделяет параметры со всеми случаями разделения (новая строка, пробел, запятая)
    После разделения убирает пробелы спереди и сзади параметра
    ПОКА НЕ Проверяет, не забыл ли пользователь разделить параметры
    Возвращает список

    Parameters
    ----------
    params : str
        Строка параметров (один или несколько) разделенных пробелом, символом новой строки, запятой, запятой с пробелом.
    one_or_none: bool
        Строка может содержать один или не содержать параметра.
    """

    pass


def split_params(params):
    """
    Разделяет параметры по новой строке
    Возвращает список
    """

    if "\n" in params:
        return [
            param.strip()
            for param in list(
                filter(
                    bool,
                    params.split(
                        "\n",
                    ),
                )
            )
        ]
    if params == "":
        return []
    return [params.strip()]


def print_in_column(task):
    print(100 * "-")
    print()
    print(f"Номер строки: {task.row_number}")
    for index in range(len(column_names)):
        print(
            column_names[index]
            + ": "
            + (",\n" + (len(column_names[index]) + 2) * " ").join(task.params[index])
        )


def print_empty_fields(task):
    print(
        str(task.row_number)
        + " ("
        + " ".join(task.task_key)
        + "): "
        + ", ".join(task.empty_params_names())
    )


class JiraTask:
    """
    Класс задачи из Jira
    Конструктору должны поступать 12 параметров в строгом порядке
    """

    def __init__(
        self,
        log_config,
        row_number,
        task_key,
        task_id,
        task_type,
        status,
        subject,
        fix_in_versions,
        update_action,
        yml_link,
        git_branch,
        report_template,
        db_objects,
    ):
        logging.config.dictConfig(log_config)
        self._logger = logging.getLogger(__name__)

        self.row_number = row_number

        self.task_key = split_params(task_key)
        self.task_id = split_params(task_id)
        self.task_type = split_params(task_type)
        self.status = split_params(status)
        self.subject = split_params(subject)
        self.fix_in_versions = split_params(fix_in_versions)
        self.update_action = split_params(update_action)
        self.yml_link = split_params(yml_link)
        self.git_branch = split_params(git_branch)
        self.report_template = split_params(report_template)
        self.db_objects = split_params(db_objects)

        self.report_ms = []
        self.report_pg = []
        self.distribute_reports(self.report_template)

        self.db_objects_ms = []
        self.db_objects_pg = []
        self.distribute_db_object(self.db_objects)

        self.params = [
            self.task_key,
            self.task_id,
            self.task_type,
            self.status,
            self.subject,
            self.fix_in_versions,
            self.update_action,
            self.yml_link,
            self.git_branch,
            self.report_template,
            self.report_ms,
            self.report_pg,
            self.db_objects,
            self.db_objects_ms,
            self.db_objects_pg,
        ]

    def check_required_params(self):
        empty_params = self.get_empty_required_params()

        if empty_params:
            self._logger.error(
                f"Строка {self.row_number}, задача {self.task_key}: Нет значений в обязательных полях: {', '.join(empty_params)}"
            )

    def get_empty_required_params(self):
        """
        Проверить обязательные поля
        :param self: Задача из Jira
        :return: Ничего
        """
        empty_required_params = []
        if not self.update_action:
            empty_required_params.append("Действия при обновлении")
        if not self.report_template:
            empty_required_params.append("Шаблоны отчетов")

        return empty_required_params

    def distribute_reports(self, reports):
        for report in reports:
            if "_pg." in report.lower():
                self.report_pg.append(report)
            else:
                self.report_ms.append(report)

    def distribute_db_object(self, db_object):
        for db_object in db_object:
            if "_pg" in db_object.lower()[-3:]:
                self.db_objects_pg.append(db_object)
            else:
                self.db_objects_ms.append(db_object)

    def __str__(self):
        return ", ".join(
            ["Задача " + str(self.row_number), *self.task_key, *self.subject]
        )

    def empty_params_names(self):
        return [
            column_index_to_name[index]
            for index, param in enumerate(self.params)
            if not param
        ]

    def empty_params_indexes(self):
        return [index for index, param in enumerate(self.params) if param[0] == ""]
