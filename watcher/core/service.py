import os

import channels
import config
import constants

from . import autostart
from .controller import WatcherController
from .history_store import load_history
from .runtime_store import load_state


class WatcherService(object):
    def __init__(self):
        self.controller = WatcherController()

    def get_status_payload(self):
        cfg = config.load_config()
        state = load_state()
        history = load_history()
        last_event = history[-1] if history else None
        enabled_channels = [item for item in cfg.get("channels", []) if item.get("enabled", True)]
        return {
            "watcher_running": self.controller.is_running(),
            "autostart_enabled": autostart.is_enabled(),
            "config_path": config.get_config_path(),
            "runtime_state_path": config.get_runtime_state_path(),
            "plugin_log_path": config.get_plugin_log_path(),
            "watcher_log_path": config.get_watcher_log_path(),
            "enabled_channel_count": len(enabled_channels),
            "last_event": last_event,
            "state": state,
        }

    def get_notification_defaults(self):
        base = config.default_config().get("notification", {})
        return base.get("templates", {})

    def get_config_payload(self):
        return config.load_config()

    def save_config_payload(self, payload, script_path=None):
        valid, message = config.validate_config(payload)
        if not valid:
            return False, message
        config.save_config(payload)
        watcher_data = payload.get("watcher", {})
        enabled = bool(watcher_data.get("start_with_windows", False))
        if script_path:
            if enabled:
                autostart.enable(script_path)
            else:
                autostart.disable()
        return True, ""

    def get_history_payload(self):
        return load_history()

    def get_logs_payload(self):
        return {
            "plugin_log": self._read_file(config.get_plugin_log_path()),
            "watcher_log": self._read_file(config.get_watcher_log_path()),
        }

    def start_watcher(self):
        return self.controller.start()

    def stop_watcher(self):
        return self.controller.stop()

    def tick_once(self):
        self.controller.tick_once()

    def test_send(self):
        cfg = config.load_config()
        valid, message = config.validate_config(cfg)
        if not valid:
            return False, message
        test_text = channels.build_message(
            constants.EVENT_TEST,
            cfg.get("machine_name", "C4D-Workstation"),
            "Config Test",
            cfg.get("notification"),
        )
        failures = channels.send_all(cfg.get("channels", []), test_text)
        if failures:
            return False, "\n".join(failures)
        return True, ""

    def _read_file(self, path):
        if not os.path.exists(path):
            return ""
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return handle.read()
        except Exception as exc:
            return "Failed to read file: {0}".format(exc)
