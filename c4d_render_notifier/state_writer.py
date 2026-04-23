import datetime
import os

import c4d

import config


def _iso_now():
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")


def _guess_output_path():
    try:
        doc = c4d.documents.GetActiveDocument()
        if doc is None:
            return ""
        render_data = doc.GetActiveRenderData()
        if render_data is None:
            return ""
        output_path = render_data[c4d.RDATA_PATH]
        if not output_path:
            return ""
        return str(output_path)
    except Exception:
        return ""


def begin_task(machine_name, project_name, render_mode, timeout_seconds):
    task_id = "{0}_{1}_{2}".format(
        datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        render_mode,
        project_name.replace(" ", "_"),
    )
    state = config.default_runtime_state()
    state.update(
        {
            "machine_name": machine_name,
            "task_id": task_id,
            "project_name": project_name,
            "render_mode": render_mode,
            "status": "running",
            "started_at": _iso_now(),
            "last_heartbeat_at": _iso_now(),
            "ended_at": "",
            "output_path": _guess_output_path(),
            "timeout_seconds": timeout_seconds,
            "timeout_notified": False,
            "completion_notified": False,
        }
    )
    config.save_runtime_state(state)
    return task_id


def heartbeat():
    state = config.load_runtime_state()
    if state.get("status") != "running":
        return
    state["last_heartbeat_at"] = _iso_now()
    output_path = _guess_output_path()
    if output_path:
        state["output_path"] = output_path
    config.save_runtime_state(state)


def mark_timeout_notified():
    state = config.load_runtime_state()
    state["timeout_notified"] = True
    state["last_heartbeat_at"] = _iso_now()
    config.save_runtime_state(state)


def mark_completed():
    state = config.load_runtime_state()
    if state.get("status") != "running":
        return
    state["status"] = "completed"
    state["ended_at"] = _iso_now()
    state["last_heartbeat_at"] = _iso_now()
    config.save_runtime_state(state)


def mark_idle(machine_name, timeout_seconds):
    config.reset_runtime_state(machine_name=machine_name, timeout_seconds=timeout_seconds)

