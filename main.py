import sys
import csv
import gitlab


def split_param(param):
    if '\n' in param:
        return param.split('\n')
    return [param]


column_names = ['Тип задачи', 'Статус', 'Тема', 'Исправить в версиях', 'Действия при обновлении',
                'Ссылка на yml', 'Ветка в Git', 'Шаблоны отчетов', 'Объекты в БД']

column_index_to_name = {
    0: 'Тип задачи',
    1: 'Статус',
    2: 'Тема',
    3: 'Исправить в версиях',
    4: 'Действия при обновлении',
    5: 'Ссылка на yml',
    6: 'Ветка в Git',
    7: 'Шаблоны отчетов',
    8: 'Объекты в БД'
}


class RowCSV:

    def __init__(self, row_number, task_type, status, subject, fix_in_versions, update_action, yml_link, git_branch,
                 report_template, db_objects):
        self.row_number = row_number

        self.task_type = split_param(task_type)
        self.status = split_param(status)
        self.subject = split_param(subject)
        self.fix_in_versions = split_param(fix_in_versions)
        self.update_action = split_param(update_action)
        self.yml_link = split_param(yml_link)
        self.git_branch = split_param(git_branch)
        self.report_template = split_param(report_template)
        self.db_objects = split_param(db_objects)

        self.params = [self.task_type, self.status, self.subject, self.fix_in_versions, self.update_action,
                       self.yml_link, self.git_branch, self.report_template, self.db_objects]

    def __str__(self):
        return str(self.row_number) + ' ' + ','.join(self.params)

    def print_in_line(self):
        pass

    def print_in_column(self):
        print(100 * '-')
        print()
        print(f'Номер строки: {self.row_number}')
        for index in range(len(column_names)):
            print(column_names[index] + ': ' + (',\n' + (len(column_names[index]) + 2) * ' ').join(
                self.params[index]))

    def empty_params_names(self):
        return [column_index_to_name[index] for index, param in enumerate(self.params) if param[0] == '']

    def empty_params_indexes(self):
        return [index for index, param in enumerate(self.params) if param[0] == '']


def read_file(file_name):
    file = open(file_name, encoding='utf-8')
    reader = csv.reader(file, delimiter=",")

    csv_rows = []

    for row_num, line in enumerate(reader):
        csv_rows.append(RowCSV(row_num, *line))

    for row in csv_rows:
        row.print_in_column()

    file.close()


def main(argv):
    print(argv)
    read_file(argv[0])

if __name__ == "__main__":
    main(sys.argv[1:])
