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
    "Объекты в БД",
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
    10: "Объекты в БД",
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
        return [param for param in params.split("\n")]
    return [params]


class JiraTask:
    def __init__(
        self,
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
            self.db_objects,
        ]

    def __str__(self):
        return ", ".join(
            ["Задача " + str(self.row_number), *self.task_key, *self.subject]
        )

    def print_in_column(self):
        print(100 * "-")
        print()
        print(f"Номер строки: {self.row_number}")
        for index in range(len(column_names)):
            print(
                column_names[index]
                + ": "
                + (',\n' + (len(column_names[index]) + 2) * " ").join(self.params[index])
            )

    def empty_params_names(self):
        return [
            column_index_to_name[index]
            for index, param in enumerate(self.params)
            if param[0] == ""
        ]

    def empty_params_indexes(self):
        return [index for index, param in enumerate(self.params) if param[0] == ""]
