import sys
import csv

from jira import JiraTask


def read_file(file_name):
    file = open(file_name, encoding="utf-8")
    reader = csv.reader(file, delimiter=",")
    next(reader)

    csv_rows = []

    for row_num, line in enumerate(reader):
        csv_rows.append(JiraTask(row_num, *line))

    for row in csv_rows:
        row.print_in_column()

    file.close()


def main(argv):
    print(argv)
    read_file(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
