import datetime

import channels
import config
import constants

from .history_store import append_history
from .logger import log
from .runtime_store import load_state


def _iso_now():
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")


def send_event(event_type, machine_name, project_name):
    current = config.load_config()
    valid, message = config.validate_config(current)
    if not valid:
        log("skip send_event because config is invalid: {0}".format(message))
        return False, message

    runtime_state = load_state()
    text = channels.build_message(event_type, machine_name, project_name, current.get("notification"), runtime_state)
    failures = channels.send_all(current["channels"], text)
    history_item = {
        "time": _iso_now(),
        "event_type": event_type,
        "machine_name": machine_name,
        "project_name": project_name,
        "success": not failures,
        "message": text,
        "failures": failures,
    }
    append_history(history_item)
    if failures:
        log("notification failed: {0}".format(" | ".join(failures)))
        return False, "\n".join(failures)
    log("notification sent: event={0}, project={1}".format(event_type, project_name))
    return True, ""


def send_test():
    current = config.load_config()
    return send_event(constants.EVENT_TEST, current.get("machine_name", "C4D-Workstation"), "Config Test")
