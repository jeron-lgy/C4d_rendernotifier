import tkinter as tk
from tkinter import messagebox, ttk

import channels
import config
import constants


class ConfiguratorApp(object):
    def __init__(self, root):
        self.root = root
        self.root.title("Tongzhi Render Notifier Configurator")
        self.root.geometry("900x620")
        self.root.minsize(800, 520)

        self.data = config.load_config()
        self.editing_index = -1

        self.machine_var = tk.StringVar()
        self.timeout_var = tk.StringVar()
        self.poll_interval_var = tk.StringVar()
        self.channel_name_var = tk.StringVar()
        self.channel_type_var = tk.StringVar()
        self.channel_endpoint_var = tk.StringVar()
        self.channel_enabled_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar()

        self.type_labels = channels.channel_type_labels()
        self.type_values = list(self.type_labels.keys())

        self._build_ui()
        self._load_all()

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)

        base = ttk.LabelFrame(container, text="Base Settings", padding=12)
        base.grid(row=0, column=0, sticky="ew")
        base.columnconfigure(1, weight=1)

        ttk.Label(base, text="Machine name").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(base, textvariable=self.machine_var).grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(base, text="Timeout seconds").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(base, textvariable=self.timeout_var, width=12).grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(base, text="Watcher poll seconds").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(base, textvariable=self.poll_interval_var, width=12).grid(row=2, column=1, sticky="w", pady=6)

        ttk.Label(base, text="Config file").grid(row=3, column=0, sticky="nw", padx=(0, 8), pady=6)
        ttk.Label(base, text=config.get_config_path(), foreground="#666").grid(row=3, column=1, sticky="w", pady=6)

        ttk.Label(base, text="Runtime state").grid(row=4, column=0, sticky="nw", padx=(0, 8), pady=6)
        ttk.Label(base, text=config.get_runtime_state_path(), foreground="#666").grid(row=4, column=1, sticky="w", pady=6)

        body = ttk.Frame(container)
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

        footer = ttk.Frame(container)
        footer.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        ttk.Button(footer, text="Save config", command=self._save_config).pack(side="left")
        ttk.Button(footer, text="Test send", command=self._test_send).pack(side="left", padx=(8, 0))
        ttk.Label(footer, textvariable=self.status_var, foreground="#666").pack(side="left", padx=(16, 0))

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
        self._refresh_channel_list()
        self._clear_channel_form()
        self.status_var.set("Config loaded")

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
        index = selection[0]
        del self.data["channels"][index]
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
        self._refresh_channel_list()
        self.status_var.set("Config saved")
        messagebox.showinfo("Done", "Config saved.")

    def _test_send(self):
        payload = self._collect_config()
        valid, message = config.validate_config(payload)
        if not valid:
            messagebox.showerror("Config error", message)
            return
        test_text = channels.build_message(constants.EVENT_TEST, payload["machine_name"], "Config Test")
        failures = channels.send_all(payload["channels"], test_text)
        if failures:
            messagebox.showerror("Test failed", "\n".join(failures))
            self.status_var.set("Test failed")
            return
        self.status_var.set("Test sent")
        messagebox.showinfo("Done", "Test message sent.")


def main():
    root = tk.Tk()
    try:
        style = ttk.Style(root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    ConfiguratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

