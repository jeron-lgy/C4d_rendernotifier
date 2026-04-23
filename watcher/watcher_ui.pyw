import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, ttk


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PLUGIN_SHARED_DIR = os.path.join(BASE_DIR, "c4d_render_notifier")
if PLUGIN_SHARED_DIR not in sys.path:
    sys.path.insert(0, PLUGIN_SHARED_DIR)

import channels
import config
import constants

from core import autostart
from core.controller import WatcherController
from core.history_store import load_history
from core.notifier import send_test
from core.runtime_store import load_state
from core.tray_manager import TrayManager


class WatcherApp(object):
    def __init__(self, root):
        self.root = root
        self.root.title("Tongzhi Watcher")
        self.root.geometry("980x720")
        self.root.minsize(860, 620)

        self.controller = WatcherController()
        self.tray = TrayManager(self)
        self.data = config.load_config()
        self.editing_index = -1

        self.machine_var = tk.StringVar()
        self.timeout_var = tk.StringVar()
        self.poll_interval_var = tk.StringVar()
        self.start_with_windows_var = tk.BooleanVar(value=False)
        self.channel_name_var = tk.StringVar()
        self.channel_type_var = tk.StringVar()
        self.channel_endpoint_var = tk.StringVar()
        self.channel_enabled_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar()
        self.runtime_summary_var = tk.StringVar()
        self.watcher_summary_var = tk.StringVar()

        self.type_labels = channels.channel_type_labels()
        self.type_values = list(self.type_labels.keys())

        self._build_ui()
        self._load_all()
        self._setup_window_behavior()
        self._schedule_refresh()

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)

        topbar = ttk.Frame(container)
        topbar.grid(row=0, column=0, sticky="ew")
        ttk.Button(topbar, text="Start watcher", command=self._start_watcher).pack(side="left")
        ttk.Button(topbar, text="Stop watcher", command=self._stop_watcher).pack(side="left", padx=(8, 0))
        ttk.Button(topbar, text="Run one tick", command=self._tick_once).pack(side="left", padx=(8, 0))
        ttk.Button(topbar, text="Test send", command=self._test_send).pack(side="left", padx=(8, 0))
        ttk.Button(topbar, text="Open data dir", command=self._open_data_dir).pack(side="left", padx=(8, 0))
        ttk.Checkbutton(
            topbar,
            text="Start with Windows",
            variable=self.start_with_windows_var,
            command=self._toggle_autostart,
        ).pack(side="left", padx=(12, 0))
        ttk.Label(topbar, textvariable=self.watcher_summary_var, foreground="#666").pack(side="left", padx=(16, 0))

        tray_note = ttk.Label(topbar, text="Close window to minimize to tray when available", foreground="#666")
        tray_note.pack(side="right")

        notebook = ttk.Notebook(container)
        notebook.grid(row=1, column=0, sticky="nsew", pady=(12, 0))

        self.config_tab = ttk.Frame(notebook, padding=12)
        self.status_tab = ttk.Frame(notebook, padding=12)
        self.history_tab = ttk.Frame(notebook, padding=12)
        self.logs_tab = ttk.Frame(notebook, padding=12)

        notebook.add(self.config_tab, text="Config")
        notebook.add(self.status_tab, text="Status")
        notebook.add(self.history_tab, text="History")
        notebook.add(self.logs_tab, text="Logs")

        self._build_config_tab()
        self._build_status_tab()
        self._build_history_tab()
        self._build_logs_tab()

        footer = ttk.Frame(container)
        footer.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        ttk.Button(footer, text="Save config", command=self._save_config).pack(side="left")
        ttk.Button(footer, text="Reload config", command=self._reload_from_disk).pack(side="left", padx=(8, 0))
        ttk.Label(footer, textvariable=self.status_var, foreground="#666").pack(side="left", padx=(16, 0))

    def _build_config_tab(self):
        self.config_tab.columnconfigure(0, weight=1)
        self.config_tab.rowconfigure(1, weight=1)

        base = ttk.LabelFrame(self.config_tab, text="Base Settings", padding=12)
        base.grid(row=0, column=0, sticky="ew")
        base.columnconfigure(1, weight=1)

        ttk.Label(base, text="Machine name").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(base, textvariable=self.machine_var).grid(row=0, column=1, sticky="ew", pady=6)
        ttk.Label(base, text="Timeout seconds").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(base, textvariable=self.timeout_var, width=12).grid(row=1, column=1, sticky="w", pady=6)
        ttk.Label(base, text="Watcher poll seconds").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(base, textvariable=self.poll_interval_var, width=12).grid(row=2, column=1, sticky="w", pady=6)
        ttk.Checkbutton(
            base,
            text="Start watcher UI with Windows",
            variable=self.start_with_windows_var,
            command=self._toggle_autostart,
        ).grid(row=3, column=1, sticky="w", pady=6)

        body = ttk.Frame(self.config_tab)
        body.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        left = ttk.LabelFrame(body, text="Channels", padding=12)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)

        self.channel_list = tk.Listbox(left, exportselection=False)
        self.channel_list.grid(row=0, column=0, sticky="nsew")
        self.channel_list.bind("<<ListboxSelect>>", self._on_select_channel)

        list_buttons = ttk.Frame(left)
        list_buttons.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        ttk.Button(list_buttons, text="New channel", command=self._new_channel).pack(side="left")
        ttk.Button(list_buttons, text="Delete channel", command=self._delete_channel).pack(side="left", padx=(8, 0))

        right = ttk.LabelFrame(body, text="Channel Editor", padding=12)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(1, weight=1)

        ttk.Label(right, text="Channel name").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(right, textvariable=self.channel_name_var).grid(row=0, column=1, sticky="ew", pady=6)
        ttk.Label(right, text="Channel type").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Combobox(
            right,
            textvariable=self.channel_type_var,
            values=[self.type_labels[key] for key in self.type_values],
            state="readonly",
        ).grid(row=1, column=1, sticky="ew", pady=6)
        ttk.Label(right, text="Webhook / SendKey").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(right, textvariable=self.channel_endpoint_var).grid(row=2, column=1, sticky="ew", pady=6)
        ttk.Checkbutton(right, text="Enable this channel", variable=self.channel_enabled_var).grid(
            row=3, column=1, sticky="w", pady=6
        )

        edit_buttons = ttk.Frame(right)
        edit_buttons.grid(row=4, column=1, sticky="w", pady=(12, 0))
        ttk.Button(edit_buttons, text="Save channel", command=self._save_channel).pack(side="left")
        ttk.Button(edit_buttons, text="Clear editor", command=self._clear_channel_form).pack(side="left", padx=(8, 0))

    def _build_status_tab(self):
        self.status_tab.columnconfigure(0, weight=1)
        runtime = ttk.LabelFrame(self.status_tab, text="Runtime Summary", padding=12)
        runtime.pack(fill="x")
        ttk.Label(runtime, textvariable=self.runtime_summary_var, justify="left").pack(anchor="w")

        paths = ttk.LabelFrame(self.status_tab, text="Shared Paths", padding=12)
        paths.pack(fill="x", pady=(12, 0))
        ttk.Label(paths, text="Config: " + config.get_config_path(), justify="left").pack(anchor="w")
        ttk.Label(paths, text="Runtime state: " + config.get_runtime_state_path(), justify="left").pack(anchor="w")
        ttk.Label(paths, text="Plugin log: " + config.get_plugin_log_path(), justify="left").pack(anchor="w")
        ttk.Label(paths, text="Watcher log: " + config.get_watcher_log_path(), justify="left").pack(anchor="w")

    def _build_history_tab(self):
        self.history_tab.columnconfigure(0, weight=1)
        self.history_tab.rowconfigure(0, weight=1)
        self.history_text = tk.Text(self.history_tab, wrap="word")
        self.history_text.grid(row=0, column=0, sticky="nsew")

    def _build_logs_tab(self):
        self.logs_tab.columnconfigure(0, weight=1)
        self.logs_tab.rowconfigure(1, weight=1)
        toolbar = ttk.Frame(self.logs_tab)
        toolbar.grid(row=0, column=0, sticky="ew")
        ttk.Button(toolbar, text="Reload logs", command=self._refresh_logs).pack(side="left")
        ttk.Button(toolbar, text="Open plugin log", command=lambda: self._open_file(config.get_plugin_log_path())).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(toolbar, text="Open watcher log", command=lambda: self._open_file(config.get_watcher_log_path())).pack(
            side="left", padx=(8, 0)
        )
        self.logs_text = tk.Text(self.logs_tab, wrap="word")
        self.logs_text.grid(row=1, column=0, sticky="nsew", pady=(12, 0))

    def _channel_type_key_from_label(self, label):
        for key, value in self.type_labels.items():
            if value == label:
                return key
        return self.type_values[0]

    def _channel_label(self, channel):
        state = "Enabled" if channel.get("enabled", True) else "Disabled"
        return "{0} | {1} | {2}".format(
            channel.get("name", "Unnamed"),
            self.type_labels.get(channel.get("type"), "Unknown type"),
            state,
        )

    def _load_all(self):
        self.machine_var.set(self.data.get("machine_name", ""))
        self.timeout_var.set(str(self.data.get("timeout_seconds", constants.DEFAULT_TIMEOUT_SECONDS)))
        watcher_data = self.data.get("watcher", {})
        self.poll_interval_var.set(str(watcher_data.get("poll_interval_seconds", constants.WATCHER_POLL_INTERVAL_SECONDS)))
        self.start_with_windows_var.set(bool(watcher_data.get("start_with_windows", False) or autostart.is_enabled()))
        self._refresh_channel_list()
        self._clear_channel_form()
        self.status_var.set("Config loaded")
        self._refresh_runtime_summary()
        self._refresh_history()
        self._refresh_logs()

    def _reload_from_disk(self):
        self.data = config.load_config()
        self._load_all()

    def _setup_window_behavior(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close_requested)
        tray_ok = self.tray.start()
        if tray_ok:
            self.status_var.set("Tray is active")
        else:
            self.status_var.set("Tray not available. Install pystray and pillow to enable it.")

    def _refresh_channel_list(self):
        self.channel_list.delete(0, tk.END)
        for channel in self.data.get("channels", []):
            self.channel_list.insert(tk.END, self._channel_label(channel))

    def _new_channel(self):
        self.editing_index = -1
        self._clear_channel_form()

    def _clear_channel_form(self):
        self.channel_name_var.set("")
        self.channel_type_var.set(self.type_labels[self.type_values[0]])
        self.channel_endpoint_var.set("")
        self.channel_enabled_var.set(True)

    def _on_select_channel(self, event=None):
        selection = self.channel_list.curselection()
        if not selection:
            return
        index = selection[0]
        self.editing_index = index
        channel = self.data["channels"][index]
        self.channel_name_var.set(channel.get("name", ""))
        self.channel_type_var.set(self.type_labels.get(channel.get("type"), self.type_labels[self.type_values[0]]))
        self.channel_endpoint_var.set(channel.get("endpoint", ""))
        self.channel_enabled_var.set(channel.get("enabled", True))

    def _current_channel_data(self):
        return {
            "name": self.channel_name_var.get().strip(),
            "type": self._channel_type_key_from_label(self.channel_type_var.get().strip()),
            "endpoint": self.channel_endpoint_var.get().strip(),
            "enabled": bool(self.channel_enabled_var.get()),
        }

    def _save_channel(self):
        item = self._current_channel_data()
        if not item["name"]:
            messagebox.showerror("Error", "Channel name is required.")
            return
        if not item["endpoint"]:
            messagebox.showerror("Error", "Webhook endpoint or SendKey is required.")
            return

        if self.editing_index < 0 or self.editing_index >= len(self.data["channels"]):
            self.data["channels"].append(item)
            self.editing_index = len(self.data["channels"]) - 1
        else:
            self.data["channels"][self.editing_index] = item

        self._refresh_channel_list()
        self.channel_list.selection_clear(0, tk.END)
        self.channel_list.selection_set(self.editing_index)
        self.status_var.set("Channel saved")

    def _delete_channel(self):
        selection = self.channel_list.curselection()
        if not selection:
            return
        del self.data["channels"][selection[0]]
        self.editing_index = -1
        self._refresh_channel_list()
        self._clear_channel_form()
        self.status_var.set("Channel deleted")

    def _collect_config(self):
        payload = {
            "machine_name": self.machine_var.get().strip(),
            "timeout_seconds": self.timeout_var.get().strip(),
            "channels": self.data.get("channels", []),
            "watcher": {
                "poll_interval_seconds": self.poll_interval_var.get().strip(),
                "start_with_windows": bool(self.start_with_windows_var.get()),
            },
        }
        try:
            payload["timeout_seconds"] = int(payload["timeout_seconds"])
        except Exception:
            payload["timeout_seconds"] = 0
        try:
            payload["watcher"]["poll_interval_seconds"] = int(payload["watcher"]["poll_interval_seconds"])
        except Exception:
            payload["watcher"]["poll_interval_seconds"] = constants.WATCHER_POLL_INTERVAL_SECONDS
        return payload

    def _save_config(self):
        payload = self._collect_config()
        valid, message = config.validate_config(payload)
        if not valid:
            messagebox.showerror("Config error", message)
            return
        config.save_config(payload)
        self.data = config.load_config()
        self._sync_autostart_setting()
        self._refresh_runtime_summary()
        self.status_var.set("Config saved")
        messagebox.showinfo("Done", "Config saved.")

    def _toggle_autostart(self):
        try:
            self._sync_autostart_setting()
            self.status_var.set("Autostart updated")
        except Exception as exc:
            self.start_with_windows_var.set(autostart.is_enabled())
            messagebox.showerror("Autostart error", str(exc))

    def _sync_autostart_setting(self):
        enabled = bool(self.start_with_windows_var.get())
        script_path = os.path.abspath(__file__)
        if enabled:
            autostart.enable(script_path)
        else:
            autostart.disable()

    def _start_watcher(self):
        started = self.controller.start()
        self.watcher_summary_var.set("Watcher running" if self.controller.is_running() else "Watcher stopped")
        if started:
            self.status_var.set("Watcher started")

    def _stop_watcher(self):
        stopped = self.controller.stop()
        self.watcher_summary_var.set("Watcher running" if self.controller.is_running() else "Watcher stopped")
        if stopped:
            self.status_var.set("Watcher stopped")

    def _tick_once(self):
        try:
            self.controller.tick_once()
            self.status_var.set("One watcher tick completed")
            self._refresh_runtime_summary()
            self._refresh_history()
            self._refresh_logs()
        except Exception as exc:
            messagebox.showerror("Watcher error", str(exc))

    def _test_send(self):
        ok, error = send_test()
        if ok:
            self.status_var.set("Test sent")
            messagebox.showinfo("Done", "Test message sent.")
        else:
            self.status_var.set("Test failed")
            messagebox.showerror("Test failed", error)

    def _open_data_dir(self):
        self._open_file(config.get_data_dir())

    def _open_file(self, path):
        try:
            os.startfile(path)
        except Exception:
            try:
                subprocess.Popen(["explorer", path])
            except Exception as exc:
                messagebox.showerror("Open failed", str(exc))

    def _on_close_requested(self):
        if self.tray.is_enabled():
            self.root.withdraw()
            self.status_var.set("Window hidden to tray")
            return
        reason = self.tray.last_error() or "pystray/pillow is not available"
        messagebox.showwarning(
            "Tray unavailable",
            "Tray mode is not active, so closing this window will exit the watcher UI.\n\nReason: {0}".format(reason),
        )
        self.exit_application()

    def show_from_tray(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.status_var.set("Window restored from tray")

    def toggle_watcher_from_tray(self):
        if self.controller.is_running():
            self._stop_watcher()
        else:
            self._start_watcher()

    def exit_application(self):
        if self.controller.is_running():
            self.controller.stop()
        self.tray.stop()
        self.root.destroy()

    def _refresh_runtime_summary(self):
        state = load_state()
        lines = [
            "Watcher: {0}".format("running" if self.controller.is_running() else "stopped"),
            "Tray: {0}".format("enabled" if self.tray.is_enabled() else "unavailable"),
            "Tray reason: {0}".format(self.tray.last_error() or "OK"),
            "Autostart: {0}".format("enabled" if autostart.is_enabled() else "disabled"),
            "State status: {0}".format(state.get("status", "idle")),
            "Task ID: {0}".format(state.get("task_id", "")),
            "Project: {0}".format(state.get("project_name", "")),
            "Render mode: {0}".format(state.get("render_mode", "")),
            "Started at: {0}".format(state.get("started_at", "")),
            "Last heartbeat: {0}".format(state.get("last_heartbeat_at", "")),
            "Ended at: {0}".format(state.get("ended_at", "")),
            "Output path: {0}".format(state.get("output_path", "")),
            "Timeout notified: {0}".format(state.get("timeout_notified", False)),
            "Completion notified: {0}".format(state.get("completion_notified", False)),
        ]
        self.runtime_summary_var.set("\n".join(lines))
        self.watcher_summary_var.set("Watcher running" if self.controller.is_running() else "Watcher stopped")

    def _refresh_history(self):
        history = load_history()
        self.history_text.delete("1.0", tk.END)
        if not history:
            self.history_text.insert(tk.END, "No notification history yet.")
            return
        for item in history[-50:]:
            self.history_text.insert(
                tk.END,
                "[{0}] {1} | {2} | success={3}\n{4}\n\n".format(
                    item.get("time", ""),
                    item.get("event_type", ""),
                    item.get("project_name", ""),
                    item.get("success", False),
                    item.get("message", ""),
                ),
            )

    def _refresh_logs(self):
        sections = []
        for label, path in (("Plugin log", config.get_plugin_log_path()), ("Watcher log", config.get_watcher_log_path())):
            sections.append("== {0} ==\n".format(label))
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as handle:
                        sections.append(handle.read())
                except Exception as exc:
                    sections.append("Failed to read log: {0}\n".format(exc))
            else:
                sections.append("Log file does not exist yet.\n")
            sections.append("\n")
        self.logs_text.delete("1.0", tk.END)
        self.logs_text.insert(tk.END, "".join(sections))

    def _schedule_refresh(self):
        self._refresh_runtime_summary()
        self._refresh_history()
        self._refresh_logs()
        self.root.after(2000, self._schedule_refresh)


def main():
    root = tk.Tk()
    try:
        style = ttk.Style(root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    WatcherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
