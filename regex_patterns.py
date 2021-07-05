import regex

def match_template_pattern(value):
    """
    Проверяет соответствие отчета регулярному выражению и возвращает только имя шаблона
    :param value: строка с путем и именем файла
    :return: строка
    """
    template_pattern = r"(?:^|\d{1,3}\/)([a-zA-Z_0-9-]+\.rptdesign)$"
    match = regex.match(template_pattern, value)
    if not match:
        raise Exception("Value doesnt match template pattern")
    return match.group(1)


def split_on_delimiters(string):
    """
    Разделяет строку по [;,\n\s]+ и очищает от пустых строк
    :param string:
    :return: список строк
    """
    delimiters = regex.compile(r"[;,\n\s]+")
    items = delimiters.split(string)
    items = list(filter(bool, items))
    if not items:
        raise Exception("Empty list of items")
    return items