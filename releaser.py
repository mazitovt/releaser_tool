import argparse

from git import Repo

from jira_api import *
from logger import *
import pprint
from menu import (
    start_menu,
    save_from_server,
    read_from_file,
    check_files,
    merge_tasks,
    fetch_remotes,
)


# TODO: добавить опцию по созданию локальной ветки с именем версии
# TODO: добавить опцию: push локальную ветку версии на сервер gitlab


def get_parser():
    """Получить парсер аргументов."""
    parser = argparse.ArgumentParser(description="Tool for pushing task changes")

    subparsers = parser.add_subparsers(dest="command")

    menu_parser = subparsers.add_parser("menu", help="Start script menu.")

    fetch_parser = subparsers.add_parser("fetch", help="Fetch all remote branches.")

    save_parser = subparsers.add_parser("save", help="Save data from server to file.")
    save_parser.add_argument(
        "-v", "--version", action="store", required=True, help="Project version."
    )

    check_parser = subparsers.add_parser(
        "check", help="Read and check data from file. Merge is optional."
    )
    check_parser.add_argument(
        "-f",
        "--file",
        action="store",
        required=True,
        help="File name from csv directory.",
    )
    check_parser.add_argument(
        "-t", "--target_branch", action="store", required=True, help="Target branch."
    )
    check_parser.add_argument(
        "-m", "--merge", action="store_true", help="Merge after check."
    )

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.command == "menu":
        start_menu()
    elif args.command == "fetch":
        fetch_remotes(REPOSITORIES)
        msg = "All remotes are fetched."
        logger.info(msg)
        print(msg)
    elif args.command == "save":
        if file := save_from_server(args.version):
            print(f"New file created: {file}")
    elif args.command == "check":
        tasks = read_from_file(args.file, REPOSITORIES)
        check_files(tasks, args.target_branch, print_details=False)
        if args.merge:
            merge_tasks(tasks, args.target_branch, print_details=False)
        print(f"Task are checked" + (" and merged." if args.merge else ""))


log_config = load_json(LOG_CONF_FILE_PATH)
check_log_folder(log_config)
logging.config.dictConfig(log_config)
logger = get_logger(log_config)
logger.info(f"{'Start app':-^30}")

app_conf = load_json(APP_CONF_FILE_PATH)
CSV_DIR = app_conf["csv_dir"]
create_folder(CSV_DIR)

repo_conf = load_json(APP_CONF_FILE_PATH)["repository"]
REPOSITORIES = {
    "report_ms": Repo(repo_conf["report_ms"]),
    "report_pg": Repo(repo_conf["report_pg"]),
}

TARGET_BRANCH = load_json("app_conf.json")["repository"]["target_branch"]


try:
    main()
except Exception as e:
    print(e)
    logger.error(str(e))

logger.info(f"{'Stop app':-^30}")
