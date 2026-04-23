import datetime
import json
import urllib.parse
import urllib.request

import constants


ZH = {
    "render_completed": "\u6e32\u67d3\u5b8c\u6210",
    "render_timeout": "\u8d85\u65f6\u63d0\u9192",
    "test": "\u6d4b\u8bd5\u6d88\u606f",
    "field_event": "\u72b6\u6001",
    "field_machine": "\u673a\u5668",
    "field_project": "\u5de5\u7a0b",
    "field_time": "\u65f6\u95f4",
    "field_render_mode": "\u6e32\u67d3\u6a21\u5f0f",
    "field_output_path": "\u8f93\u51fa\u8def\u5f84",
    "field_started_at": "\u5f00\u59cb\u65f6\u95f4",
    "unnamed_machine": "\u672a\u547d\u540d\u673a\u5668",
    "unnamed_project": "\u672a\u547d\u540d\u5de5\u7a0b",
    "manual_render": "\u624b\u52a8\u6e32\u67d3",
    "queue_render": "\u6e32\u67d3\u961f\u5217",
    "title": "C4D \u901a\u77e5",
}


def channel_type_labels():
    return {
        constants.CHANNEL_TYPE_FEISHU: "Feishu Webhook",
        constants.CHANNEL_TYPE_SERVERCHAN: "ServerChan",
        constants.CHANNEL_TYPE_GENERIC: "Generic Webhook",
    }


def event_type_labels():
    return {
        constants.EVENT_RENDER_COMPLETED: ZH["render_completed"],
        constants.EVENT_RENDER_TIMEOUT: ZH["render_timeout"],
        constants.EVENT_TEST: ZH["test"],
    }


def notification_field_labels():
    return {
        constants.NOTIFICATION_FIELD_EVENT: ZH["field_event"],
        constants.NOTIFICATION_FIELD_MACHINE: ZH["field_machine"],
        constants.NOTIFICATION_FIELD_PROJECT: ZH["field_project"],
        constants.NOTIFICATION_FIELD_TIME: ZH["field_time"],
        constants.NOTIFICATION_FIELD_RENDER_MODE: ZH["field_render_mode"],
        constants.NOTIFICATION_FIELD_OUTPUT_PATH: ZH["field_output_path"],
        constants.NOTIFICATION_FIELD_STARTED_AT: ZH["field_started_at"],
    }


def _default_notification_config():
    return {
        "default_template": constants.EVENT_RENDER_COMPLETED,
        "templates": {
            constants.EVENT_RENDER_COMPLETED: {
                "fields": [
                    constants.NOTIFICATION_FIELD_EVENT,
                    constants.NOTIFICATION_FIELD_MACHINE,
                    constants.NOTIFICATION_FIELD_PROJECT,
                ],
                "separator": " | ",
                "show_labels": False,
            },
            constants.EVENT_RENDER_TIMEOUT: {
                "fields": [
                    constants.NOTIFICATION_FIELD_EVENT,
                    constants.NOTIFICATION_FIELD_MACHINE,
                    constants.NOTIFICATION_FIELD_PROJECT,
                    constants.NOTIFICATION_FIELD_RENDER_MODE,
                    constants.NOTIFICATION_FIELD_TIME,
                ],
                "separator": " | ",
                "show_labels": False,
            },
            constants.EVENT_TEST: {
                "fields": [
                    constants.NOTIFICATION_FIELD_EVENT,
                    constants.NOTIFICATION_FIELD_MACHINE,
                    constants.NOTIFICATION_FIELD_PROJECT,
                ],
                "separator": " | ",
                "show_labels": False,
            },
        },
    }


def _current_time_text():
    return datetime.datetime.now(datetime.timezone.utc).astimezone().strftime("%H:%M:%S")


def _format_iso_text(value):
    if not value:
        return ""
    try:
        return datetime.datetime.fromisoformat(value).strftime("%Y/%m/%d %H:%M:%S")
    except Exception:
        return str(value)


def _build_runtime_fields(runtime_state):
    result = {
        constants.NOTIFICATION_FIELD_RENDER_MODE: "",
        constants.NOTIFICATION_FIELD_OUTPUT_PATH: "",
        constants.NOTIFICATION_FIELD_STARTED_AT: "",
    }
    if not isinstance(runtime_state, dict):
        return result

    mode = runtime_state.get("render_mode", "")
    if mode == "manual":
        result[constants.NOTIFICATION_FIELD_RENDER_MODE] = ZH["manual_render"]
    elif mode == "queue":
        result[constants.NOTIFICATION_FIELD_RENDER_MODE] = ZH["queue_render"]
    else:
        result[constants.NOTIFICATION_FIELD_RENDER_MODE] = str(mode or "")

    result[constants.NOTIFICATION_FIELD_OUTPUT_PATH] = str(runtime_state.get("output_path", "") or "")
    result[constants.NOTIFICATION_FIELD_STARTED_AT] = _format_iso_text(runtime_state.get("started_at", ""))
    return result


def build_message(event_type, machine_name, project_name, notification_config=None, runtime_state=None):
    notification = _default_notification_config()
    if isinstance(notification_config, dict):
        if isinstance(notification_config.get("default_template"), str):
            notification["default_template"] = notification_config["default_template"]
        if isinstance(notification_config.get("templates"), dict):
            for key, template in notification_config["templates"].items():
                if isinstance(template, dict):
                    notification["templates"][key] = template

    template = notification["templates"].get(
        event_type,
        notification["templates"].get(
            notification.get("default_template", constants.EVENT_RENDER_COMPLETED),
            notification["templates"][constants.EVENT_RENDER_COMPLETED],
        ),
    )

    field_values = {
        constants.NOTIFICATION_FIELD_EVENT: event_type_labels().get(event_type, event_type),
        constants.NOTIFICATION_FIELD_MACHINE: machine_name or ZH["unnamed_machine"],
        constants.NOTIFICATION_FIELD_PROJECT: project_name or ZH["unnamed_project"],
        constants.NOTIFICATION_FIELD_TIME: _current_time_text(),
    }
    field_values.update(_build_runtime_fields(runtime_state))

    labels = notification_field_labels()
    parts = []
    for field in template.get("fields", []):
        value = field_values.get(field)
        if not value:
            continue
        if template.get("show_labels", False):
            parts.append("{0}: {1}".format(labels.get(field, field), value))
        else:
            parts.append(str(value))

    if not parts:
        parts = [
            event_type_labels().get(event_type, event_type),
            machine_name or ZH["unnamed_machine"],
            project_name or ZH["unnamed_project"],
        ]

    separator = template.get("separator", " | ") or " | "
    return separator.join(parts)


def _send_json(endpoint, payload):
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return response.getcode(), response.read()


def _send_form(endpoint, payload):
    data = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(endpoint, data=data, method="POST")
    with urllib.request.urlopen(request, timeout=10) as response:
        return response.getcode(), response.read()


def send_channel(channel, text):
    ctype = channel["type"]
    endpoint = channel["endpoint"]

    if ctype == constants.CHANNEL_TYPE_FEISHU:
        _send_json(endpoint, {"msg_type": "text", "content": {"text": text}})
        return True, ""

    if ctype == constants.CHANNEL_TYPE_SERVERCHAN:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            api_url = endpoint
        else:
            api_url = "https://sctapi.ftqq.com/{0}.send".format(endpoint)
        _send_form(api_url, {"title": ZH["title"], "desp": text})
        return True, ""

    if ctype == constants.CHANNEL_TYPE_GENERIC:
        _send_json(endpoint, {"text": text, "message": text})
        return True, ""

    return False, "Unsupported channel type: {0}".format(ctype)


def send_all(channel_items, text):
    failures = []
    for channel in channel_items:
        if not channel.get("enabled", True):
            continue
        try:
            ok, error = send_channel(channel, text)
        except Exception as exc:
            ok, error = False, str(exc)
        if not ok:
            failures.append("{0}: {1}".format(channel.get("name", "Unnamed channel"), error))
    return failures
