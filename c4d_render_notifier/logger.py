import datetime
import os

import config


def get_log_path():
    return config.get_plugin_log_path()


def log(message):
    config.ensure_data_dir()
    line = "[{0}] {1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)
    with open(get_log_path(), "a", encoding="utf-8") as handle:
        handle.write(line)

