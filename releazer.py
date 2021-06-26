import sys
import csv
import os
import logging
import argparse

from jira import JiraTask


def parse_args():
    parser = argparse.ArgumentParser(description="Tool for pushing task changes")
    parser.add_argument(
        "-f", "--file", action="store", required=True, help="File absolute path"
    )
    parser.add_argument(
        "-s",
        "--skip_headers",
        action="store_true",
        help="Skip csv file headers",
    )

    return parser.parse_args()


def file_exists(file_path):
    return os.path.exists(file_path)


def read_file(file_name, skip_headers):
    with open(file_name, encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")

        if skip_headers:
            next(reader)

        return [JiraTask(row_num, *line) for row_num, line in enumerate(reader)]


def print_empty_fields(jira_tasks):
    print("\nПустые поля в строках:")
    for jira_task in jira_tasks:
        print(
            str(jira_task.row_number) + ": " + ", ".join(jira_task.empty_params_names())
        )


def log():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.debug()


def main():
    args = parse_args()
    file_path = args.file
    skip_headers = args.skip_headers

    if not file_exists(file_path):
        print("Ошибка! Такого файла не существует")
        return

    jira_tasks = read_file(file_path, skip_headers)
    print_empty_fields(jira_tasks)

    for jira_task in jira_tasks:
        jira_task.print_in_column()


if __name__ == "__main__":
    main()
