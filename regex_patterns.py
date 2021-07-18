import regex


def match_task_name_pattern(value):
    """
    Проверяет соответствие названия задачи регулярному выражению.
    """
    task_name_pattern = r"[A-Z]+-\d+"
    task_name = regex.match(task_name_pattern, value)
    if not task_name:
        return None
    return task_name.group()


def match_branch_pattern(value):
    """
    Проверяет соответствие ветки регулярному выражению и возвращает только имя ветки и репозитория.
    """
    #                                                        1     2              3
    branch_pattern = (
        r"https://git\.promedweb\.ru/rtmis/(report_(ms|pg))/-/tree/([A-Z]+-\d+)"
    )
    branch = regex.match(branch_pattern, value)
    if not branch:
        return None
    return {"repository_name": branch.group(1), "branch_name": branch.group(3)}


def match_template_pattern(value):
    """
    Проверяет соответствие отчета регулярному выражению и возвращает только имя шаблона.
    """
    template_pattern = r"(?:^|\d{1,3}\/)([a-zA-Z_0-9-]+\.rptdesign)$"
    match = regex.match(template_pattern, value)
    if not match:
        return None
        # raise Exception("Value doesn't match template pattern.")
    return match.group(1)


def split_on_delimiters(input_string):
    """
    Разделяет строку по [;,\n\s]+ и очищает от пустых строк.
    """
    delimiters = regex.compile(r"[;,\n\s]+")
    items = delimiters.split(input_string)
    return list(filter(bool, items))
