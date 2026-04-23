import datetime
import glob
import os

import config
import constants

from .logger import log
from .notifier import send_event
from .runtime_store import load_state, save_state, update_flags


def _parse_iso(value):
    if not value:
        return None
    try:
        return datetime.datetime.fromisoformat(value)
    except Exception:
        return None


def _now():
    return datetime.datetime.now(datetime.timezone.utc).astimezone()


def _pattern_to_glob(output_path):
    if not output_path:
        return ""
    pattern = output_path
    for token in ("####", "$frame", "$F", "%04d", "%03d", "%02d", "%d"):
        pattern = pattern.replace(token, "*")
    return pattern


def _find_latest_output_time(output_path):
    if not output_path:
        return None
    pattern = _pattern_to_glob(output_path)
    candidates = []
    if "*" in pattern:
        candidates = glob.glob(pattern)
    elif os.path.exists(pattern):
        candidates = [pattern]
    if not candidates:
        return None
    latest = None
    for path in candidates:
        try:
            changed = datetime.datetime.fromtimestamp(os.path.getmtime(path), tz=datetime.timezone.utc).astimezone()
        except Exception:
            continue
        if latest is None or changed > latest:
            latest = changed
    return latest


class WatcherDetector(object):
    def __init__(self):
        self._last_seen_task_id = ""

    def poll_interval_seconds(self):
        current = config.load_config()
        watcher_data = current.get("watcher", {})
        try:
            return max(1, int(watcher_data.get("poll_interval_seconds", constants.WATCHER_POLL_INTERVAL_SECONDS)))
        except Exception:
            return constants.WATCHER_POLL_INTERVAL_SECONDS

    def tick(self):
        state = load_state()
        task_id = state.get("task_id", "")
        if task_id and task_id != self._last_seen_task_id:
            log("watcher observed task: {0}".format(task_id))
            self._last_seen_task_id = task_id

        status = state.get("status", "idle")
        if status == "running":
            self._handle_running(state)
            return
        if status == "completed":
            self._handle_completed(state)
            return

    def _handle_running(self, state):
        now = _now()
        started_at = _parse_iso(state.get("started_at"))
        heartbeat_at = _parse_iso(state.get("last_heartbeat_at"))
        timeout_seconds = int(state.get("timeout_seconds", constants.DEFAULT_TIMEOUT_SECONDS) or constants.DEFAULT_TIMEOUT_SECONDS)
        machine_name = state.get("machine_name", "C4D-Workstation")
        project_name = state.get("project_name", "Unknown Project")

        if started_at and not state.get("timeout_notified") and (now - started_at).total_seconds() >= timeout_seconds:
            ok, error = send_event(constants.EVENT_RENDER_TIMEOUT, machine_name, project_name)
            if ok:
                update_flags(timeout_notified=True)
            else:
                log("timeout notification failed: {0}".format(error))

        latest_output_time = _find_latest_output_time(state.get("output_path", ""))
        heartbeat_stale = False
        if heartbeat_at:
            heartbeat_stale = (now - heartbeat_at).total_seconds() >= constants.TASK_STALE_SECONDS

        # Fallback completion inference:
        # if the plugin heartbeat stopped for a while and output files were updated after render start,
        # treat the task as completed to reduce front-window dependency.
        if heartbeat_stale and latest_output_time and started_at and latest_output_time >= started_at:
            log("watcher inferred completion from stale heartbeat and output files")
            state["status"] = "completed"
            state["ended_at"] = latest_output_time.isoformat(timespec="seconds")
            save_state(state)
            self._handle_completed(state)

    def _handle_completed(self, state):
        if state.get("completion_notified"):
            return
        machine_name = state.get("machine_name", "C4D-Workstation")
        project_name = state.get("project_name", "Unknown Project")
        ok, error = send_event(constants.EVENT_RENDER_COMPLETED, machine_name, project_name)
        if ok:
            update_flags(completion_notified=True)
        else:
            log("completion notification failed: {0}".format(error))
