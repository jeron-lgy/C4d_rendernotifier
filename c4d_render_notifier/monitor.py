import os
import threading
import time

import c4d

import config
import constants
import logger
import state_writer


class RenderState(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.manual_active = False
        self.queue_active = False
        self.timeout_flag = False
        self.started_at = 0.0
        self.last_heartbeat_write = 0.0
        self.project_name = "Unknown Project"
        self.queue_project_name = "Render Queue"
        self.last_manual_flag = None
        self.last_queue_flag = None

    def begin(self, project_name, is_queue):
        with self.lock:
            now = time.time()
            self.started_at = now
            self.last_heartbeat_write = 0.0
            self.timeout_flag = False
            if is_queue:
                self.queue_active = True
                self.queue_project_name = project_name or "Render Queue"
            else:
                self.manual_active = True
                self.project_name = project_name or "Current Project"

    def should_write_heartbeat(self):
        with self.lock:
            if not (self.manual_active or self.queue_active):
                return False
            return (time.time() - self.last_heartbeat_write) >= constants.HEARTBEAT_INTERVAL_SECONDS

    def touch_heartbeat(self):
        with self.lock:
            self.last_heartbeat_write = time.time()

    def should_timeout(self, timeout_seconds):
        with self.lock:
            if not (self.manual_active or self.queue_active) or self.timeout_flag:
                return False
            return (time.time() - self.started_at) >= timeout_seconds

    def mark_timeout(self):
        with self.lock:
            self.timeout_flag = True

    def end(self, is_queue):
        with self.lock:
            if is_queue:
                project = self.queue_project_name
                self.queue_active = False
            else:
                project = self.project_name
                self.manual_active = False
            if not (self.manual_active or self.queue_active):
                self.started_at = 0.0
                self.last_heartbeat_write = 0.0
                self.timeout_flag = False
            return project


STATE = RenderState()


def _guess_manual_project_name():
    doc = c4d.documents.GetActiveDocument()
    if doc is None:
        return "Current Project"
    name = doc.GetDocumentName()
    if name:
        return name
    path = doc.GetDocumentPath()
    if path:
        return os.path.basename(path)
    return "Untitled"


def _guess_queue_project_name():
    try:
        batch = c4d.documents.GetBatchRender()
    except Exception:
        return "Render Queue"
    if batch is None:
        return "Render Queue"
    try:
        count = batch.GetElementCount()
    except Exception:
        return "Render Queue"
    names = []
    for index in range(count):
        try:
            if not batch.GetEnableElement(index):
                continue
            path = batch.GetElement(index)
        except Exception:
            continue
        if not path:
            continue
        names.append(os.path.basename(str(path)))
    if not names:
        return "Render Queue"
    if len(names) == 1:
        return names[0]
    return "Render Queue ({0})".format(len(names))


def _machine_and_timeout():
    current = config.load_config()
    return current.get("machine_name", "C4D-Workstation"), int(current.get("timeout_seconds", constants.DEFAULT_TIMEOUT_SECONDS))


def test_send():
    current = config.load_config()
    valid, message = config.validate_config(current)
    if not valid:
        return False, message
    return True, "Use the external watcher or configurator for test sending."


def _write_running_state(project_name, render_mode):
    machine_name, timeout_seconds = _machine_and_timeout()
    task_id = state_writer.begin_task(machine_name, project_name, render_mode, timeout_seconds)
    logger.log("state begin: task_id={0}, mode={1}, project={2}".format(task_id, render_mode, project_name))


def _write_completed_state(render_mode):
    project_name = STATE.queue_project_name if render_mode == "queue" else STATE.project_name
    state_writer.mark_completed()
    logger.log("state completed: mode={0}, project={1}".format(render_mode, project_name))


def monitor_tick():
    manual_now = False
    queue_now = False

    try:
        manual_now = c4d.CheckIsRunning(c4d.CHECKISRUNNING_EDITORRENDERING) or c4d.CheckIsRunning(
            c4d.CHECKISRUNNING_EXTERNALRENDERING
        ) or c4d.CheckIsRunning(c4d.CHECKISRUNNING_INTERACTIVERENDERING)
    except Exception:
        manual_now = False

    try:
        batch = c4d.documents.GetBatchRender()
        queue_now = bool(batch and batch.IsRendering())
    except Exception:
        queue_now = False

    if STATE.last_manual_flag is None or STATE.last_manual_flag != manual_now:
        logger.log("manual render flag changed: {0}".format(manual_now))
        STATE.last_manual_flag = manual_now
    if STATE.last_queue_flag is None or STATE.last_queue_flag != queue_now:
        logger.log("queue render flag changed: {0}".format(queue_now))
        STATE.last_queue_flag = queue_now

    if manual_now and not STATE.manual_active:
        project_name = _guess_manual_project_name()
        STATE.begin(project_name, is_queue=False)
        _write_running_state(project_name, "manual")
    elif STATE.manual_active and not manual_now:
        STATE.end(is_queue=False)
        _write_completed_state("manual")

    if queue_now and not STATE.queue_active:
        project_name = _guess_queue_project_name()
        STATE.begin(project_name, is_queue=True)
        _write_running_state(project_name, "queue")
    elif STATE.queue_active and not queue_now:
        STATE.end(is_queue=True)
        _write_completed_state("queue")

    if STATE.should_write_heartbeat():
        state_writer.heartbeat()
        STATE.touch_heartbeat()
        logger.log("state heartbeat")

    _, timeout_seconds = _machine_and_timeout()
    if STATE.should_timeout(timeout_seconds):
        STATE.mark_timeout()
        state_writer.mark_timeout_notified()
        logger.log("state timeout flagged: threshold={0}".format(timeout_seconds))

    if not STATE.manual_active and not STATE.queue_active:
        machine_name, timeout_seconds = _machine_and_timeout()
        current_state = config.load_runtime_state()
        if current_state.get("status") == "idle":
            return
        if current_state.get("status") == "completed":
            return
        state_writer.mark_idle(machine_name, timeout_seconds)
        logger.log("state reset to idle")
