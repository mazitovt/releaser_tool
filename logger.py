import os
import logging
import logging.config
import json

LOG_CONF_FILE_PATH = "logger_conf.json"
APP_CONF_FILE_PATH = "app_conf.json"


def check_log_folder(log_config):
    """Проверяет существование каталога для сохранения логов,
    если задано логгирование в файл.
    Создает каталог если он не существует.

    log_config - конфигурация логгера

    """
    try:
        file_path = log_config["handlers"]["file_handler"]["filename"]
    except Exception as ex:
        pass
    if file_path:
        folder = os.path.split(file_path)[0]
        if not os.path.isdir(folder):
            os.mkdir(folder)


def load_json(json_file_path):
    """Читает данные из json файла"""
    with open(json_file_path, "r") as conf_file:
        return json.load(conf_file)


def get_logger(log_config):
    """Создает и возвращает логгер"""
    logging.config.dictConfig(log_config)
    return logging.getLogger(__name__)
