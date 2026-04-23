import json
import os
import socket
from copy import deepcopy

import constants


def _default_machine_name():
    name = socket.gethostname().strip()
    return name or "C4D-Workstation"


def get_data_dir():
    appdata = os.environ.get("APPDATA")
    if appdata:
        return os.path.join(appdata, "TongzhiRenderNotifier")
    return os.path.join(os.path.expanduser("~"), ".tongzhi_render_notifier")


def ensure_data_dir():
    data_dir = get_data_dir()
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir


def get_config_path():
    return os.path.join(get_data_dir(), constants.SETTINGS_FILENAME)


def get_runtime_state_path():
    return os.path.join(get_data_dir(), constants.RUNTIME_STATE_FILENAME)


def get_plugin_log_path():
    return os.path.join(get_data_dir(), constants.PLUGIN_LOG_FILENAME)


def get_watcher_log_path():
    return os.path.join(get_data_dir(), constants.WATCHER_LOG_FILENAME)


def get_history_path():
    return os.path.join(get_data_dir(), constants.HISTORY_FILENAME)


def default_config():
    return {
        "machine_name": _default_machine_name(),
        "timeout_seconds": constants.DEFAULT_TIMEOUT_SECONDS,
        "channels": [],
        "notification": {
            "default_template": "render_completed",
            "templates": {
                "render_completed": {
                    "fields": [
                        constants.NOTIFICATION_FIELD_EVENT,
                        constants.NOTIFICATION_FIELD_MACHINE,
                        constants.NOTIFICATION_FIELD_PROJECT,
                    ],
                    "separator": " | ",
                    "show_labels": False,
                },
                "render_timeout": {
                    "fields": [
                        constants.NOTIFICATION_FIELD_EVENT,
                        constants.NOTIFICATION_FIELD_MACHINE,
                        constants.NOTIFICATION_FIELD_PROJECT,
                        constants.NOTIFICATION_FIELD_TIME,
                    ],
                    "separator": " | ",
                    "show_labels": False,
                },
                "test": {
                    "fields": [
                        constants.NOTIFICATION_FIELD_EVENT,
                        constants.NOTIFICATION_FIELD_MACHINE,
                        constants.NOTIFICATION_FIELD_PROJECT,
                    ],
                    "separator": " | ",
                    "show_labels": False,
                },
            },
        },
        "watcher": {
            "poll_interval_seconds": constants.WATCHER_POLL_INTERVAL_SECONDS,
            "start_with_windows": False,
        },
    }


def default_runtime_state():
    return {
        "version": 1,
        "machine_name": _default_machine_name(),
        "task_id": "",
        "project_name": "",
        "render_mode": "",
        "status": "idle",
        "started_at": "",
        "last_heartbeat_at": "",
        "ended_at": "",
        "output_path": "",
        "timeout_seconds": constants.DEFAULT_TIMEOUT_SECONDS,
        "timeout_notified": False,
        "completion_notified": False,
    }


def _normalize_channels(items):
    result = []
    for item in items:
        if not isinstance(item, dict):
            continue
        settings = item.get("settings", {})
        if not isinstance(settings, dict):
            settings = {}
        endpoint = str(item.get("endpoint", settings.get("endpoint", settings.get("sendkey", "")))).strip()
        result.append(
            {
                "name": str(item.get("name", "")).strip(),
                "type": str(item.get("type", "")).strip(),
                "endpoint": endpoint,
                "enabled": bool(item.get("enabled", True)),
            }
        )
    return result


def _normalize_notification(data):
    default = default_config()["notification"]
    template_default = default["templates"]["render_completed"]
    if not isinstance(data, dict):
        return default

    allowed_fields = {
        constants.NOTIFICATION_FIELD_EVENT,
        constants.NOTIFICATION_FIELD_MACHINE,
        constants.NOTIFICATION_FIELD_PROJECT,
        constants.NOTIFICATION_FIELD_TIME,
        constants.NOTIFICATION_FIELD_RENDER_MODE,
        constants.NOTIFICATION_FIELD_OUTPUT_PATH,
        constants.NOTIFICATION_FIELD_STARTED_AT,
    }
    def normalize_template(item, fallback):
        raw_fields = item.get("fields", fallback["fields"]) if isinstance(item, dict) else fallback["fields"]
        normalized_fields = []
        if isinstance(raw_fields, list):
            for raw in raw_fields:
                field = str(raw).strip()
                if field in allowed_fields and field not in normalized_fields:
                    normalized_fields.append(field)
        if not normalized_fields:
            normalized_fields = list(fallback["fields"])

        separator = str(item.get("separator", fallback["separator"])) if isinstance(item, dict) else fallback["separator"]
        if not separator:
            separator = fallback["separator"]
        if len(separator) > 10:
            separator = separator[:10]

        return {
            "fields": normalized_fields,
            "separator": separator,
            "show_labels": bool(item.get("show_labels", fallback["show_labels"])) if isinstance(item, dict) else fallback["show_labels"],
        }

    templates_input = data.get("templates")
    templates = {}
    if isinstance(templates_input, dict):
        for key, fallback in default["templates"].items():
            templates[key] = normalize_template(templates_input.get(key, {}), fallback)
    else:
        # Backward compatibility with the old single-template structure.
        legacy_template = normalize_template(data, template_default)
        templates = {
            "render_completed": normalize_template({}, default["templates"]["render_completed"]),
            "render_timeout": normalize_template({}, default["templates"]["render_timeout"]),
            "test": normalize_template({}, default["templates"]["test"]),
        }
        templates["render_completed"] = legacy_template
        templates["test"] = legacy_template

    default_template = str(data.get("default_template", default["default_template"])).strip()
    if default_template not in templates:
        default_template = default["default_template"]

    return {
        "default_template": default_template,
        "templates": templates,
    }


def normalize_config(data):
    result = deepcopy(default_config())
    if not isinstance(data, dict):
        return result

    result["machine_name"] = str(data.get("machine_name", result["machine_name"])).strip() or result["machine_name"]

    try:
        result["timeout_seconds"] = int(data.get("timeout_seconds", result["timeout_seconds"]))
    except Exception:
        result["timeout_seconds"] = constants.DEFAULT_TIMEOUT_SECONDS

    result["channels"] = _normalize_channels(data.get("channels", []))
    result["notification"] = _normalize_notification(data.get("notification", {}))

    watcher_data = data.get("watcher", {})
    if not isinstance(watcher_data, dict):
        watcher_data = {}
    try:
        poll_interval = int(watcher_data.get("poll_interval_seconds", constants.WATCHER_POLL_INTERVAL_SECONDS))
    except Exception:
        poll_interval = constants.WATCHER_POLL_INTERVAL_SECONDS
    result["watcher"] = {
        "poll_interval_seconds": max(1, poll_interval),
        "start_with_windows": bool(watcher_data.get("start_with_windows", False)),
    }
    return result


def load_config():
    path = get_config_path()
    if not os.path.exists(path):
        return default_config()

    try:
        with open(path, "r", encoding="utf-8") as handle:
            loaded = json.load(handle)
    except Exception:
        return default_config()

    return normalize_config(loaded)


def save_config(data):
    ensure_data_dir()
    normalized = normalize_config(data)
    with open(get_config_path(), "w", encoding="utf-8") as handle:
        json.dump(normalized, handle, ensure_ascii=False, indent=2)


def load_runtime_state():
    path = get_runtime_state_path()
    if not os.path.exists(path):
        return default_runtime_state()

    try:
        with open(path, "r", encoding="utf-8") as handle:
            loaded = json.load(handle)
    except Exception:
        return default_runtime_state()

    state = default_runtime_state()
    if isinstance(loaded, dict):
        state.update(loaded)
    return state


def save_runtime_state(data):
    ensure_data_dir()
    state = default_runtime_state()
    if isinstance(data, dict):
        state.update(data)
    with open(get_runtime_state_path(), "w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=False, indent=2)


def reset_runtime_state(machine_name=None, timeout_seconds=None):
    state = default_runtime_state()
    if machine_name:
        state["machine_name"] = machine_name
    if timeout_seconds:
        state["timeout_seconds"] = timeout_seconds
    save_runtime_state(state)


def validate_config(data):
    normalized = normalize_config(data)
    if not normalized["machine_name"]:
        return False, "Machine name is required."
    if normalized["timeout_seconds"] <= 0:
        return False, "Timeout seconds must be greater than 0."
    enabled_channels = [item for item in normalized["channels"] if item["enabled"]]
    if not enabled_channels:
        return False, "At least one enabled channel is required."
    templates = normalized.get("notification", {}).get("templates", {})
    for template in templates.values():
        if not template.get("fields"):
            return False, "At least one notification field is required."
    for channel in enabled_channels:
        if not channel["name"]:
            return False, "Channel name is required."
        if not channel["type"]:
            return False, "Channel type is required."
        if not channel["endpoint"]:
            return False, "Channel endpoint or key is required."
    return True, ""
