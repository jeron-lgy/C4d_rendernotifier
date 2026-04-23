import json
import os

import config


def load_history():
    path = config.get_history_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        return []
    if isinstance(data, list):
        return data
    return []


def append_history(item, limit=50):
    config.ensure_data_dir()
    history = load_history()
    history.append(item)
    history = history[-limit:]
    with open(config.get_history_path(), "w", encoding="utf-8") as handle:
        json.dump(history, handle, ensure_ascii=False, indent=2)

