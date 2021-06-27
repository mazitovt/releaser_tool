import sys
import csv
import os
import logging
import argparse

from logger import *
from jira import *


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

    parser.add_argument(
        "-e",
        "--empty_columns",
        action="store_true",
        help="Show empty columns for each task",
    )

    parser.add_argument(
        "-sh", "--show_parsed", action="store_true", help="Show parsed tasks"
    )

    return parser.parse_args()


def file_exists(file_path):
    return os.path.exists(file_path)


def read_file(file_name, skip_headers):
    with open(file_name, encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")

        if skip_headers:
            next(reader)

        return [JiraTask(log_config, row_num, *line) for row_num, line in enumerate(reader)]






def main():


    args = parse_args()
    file_path = args.file
    skip_headers = args.skip_headers
    empty_columns = args.empty_columns
    show_parsed = args.show_parsed

    if not file_exists(file_path):
        print("Ошибка! Такого файла не существует")
        return

    jira_tasks = read_file(file_path, skip_headers)

    if empty_columns:
        print("\nПустые поля в задачах:")
        for task in jira_tasks:
            print_empty_fields(task)

    if show_parsed:
        print("\nВсе поля в задачах:")
        for task in jira_tasks:
            print_in_column(task)


log_config = load_json(LOG_CONF_FILE_PATH)
check_log_folder(log_config)
logger = get_logger(log_config)
logger.debug('Start app')
main()
