import os
import subprocess
import sys


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

from PySide6 import QtCore, QtGui, QtWidgets


APP_STYLE = """
QWidget {
  background: #f2f2f2;
  color: #14131a;
  font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
  font-size: 13px;
}
QMainWindow { background: #f2f2f2; }
#RootFrame { background: #f2f2f2; }
#Sidebar, #MainSurface {
  background: rgba(255,255,255,0.92);
  border: 1px solid rgba(20,19,26,0.08);
  border-radius: 28px;
}
#BrandMark {
  background: #249782;
  color: white;
  border-radius: 16px;
  font-size: 24px;
  font-weight: 800;
}
QPushButton {
  background: #ebe9e8;
  border: none;
  border-radius: 14px;
  padding: 12px 18px;
  font-weight: 700;
}
QPushButton:hover { background: #e1dfde; }
QPushButton[primary="true"] {
  background: #249782;
  color: white;
}
QPushButton[primary="true"]:hover { background: #1e7f6d; }
QPushButton[nav="true"] {
  text-align: left;
  padding: 14px 16px;
  border-radius: 16px;
  background: transparent;
}
QPushButton[nav="true"][active="true"] {
  background: #14131a;
  color: white;
}
QLineEdit, QSpinBox, QPlainTextEdit, QListWidget, QComboBox {
  background: #fbfbfb;
  border: 1px solid rgba(20,19,26,0.08);
  border-radius: 14px;
  padding: 8px 10px;
}
QPlainTextEdit {
  selection-background-color: rgba(36,151,130,0.18);
}
QScrollBar:vertical {
  background: transparent;
  width: 10px;
  margin: 6px 0 6px 0;
}
QScrollBar::handle:vertical {
  background: rgba(20,19,26,0.16);
  border-radius: 5px;
  min-height: 30px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
  background: transparent;
  height: 0px;
}
QLabel[eyebrow="true"] {
  color: #7f7b85;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}
QLabel[title="true"] {
  font-size: 24px;
  font-weight: 800;
}
QLabel[heroTitle="true"] {
  color: white;
  font-size: 28px;
  font-weight: 800;
}
QLabel[heroSub="true"] {
  color: rgba(255,255,255,0.78);
}
QLabel[muted="true"] { color: #7f7b85; }
"""


def make_label(text="", **props):
    label = QtWidgets.QLabel(text)
    for key, value in props.items():
        label.setProperty(key, value)
    return label


class NavButton(QtWidgets.QPushButton):
    clicked_page = QtCore.Signal(str)

    def __init__(self, page_name, text):
        super().__init__(text)
        self.page_name = page_name
        self.setProperty("nav", True)
        self.setProperty("active", False)
        self.clicked.connect(lambda: self.clicked_page.emit(self.page_name))

    def set_active(self, active):
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


class StatusBadge(QtWidgets.QLabel):
    def __init__(self, text="", kind="dark"):
        super().__init__(text)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMinimumHeight(34)
        self.setContentsMargins(12, 6, 12, 6)
        self.set_kind(kind)

    def set_kind(self, kind):
        if kind == "green":
            self.setStyleSheet("background: rgba(255,255,255,0.16); color: white; border-radius: 999px; font-weight: 800; padding: 8px 14px;")
        elif kind == "light":
            self.setStyleSheet("background: rgba(36,151,130,0.12); color: #249782; border-radius: 999px; font-weight: 800; padding: 8px 14px;")
        else:
            self.setStyleSheet("background: #eceae9; color: #14131a; border-radius: 999px; font-weight: 800; padding: 8px 14px;")


class MetricCard(QtWidgets.QFrame):
    def __init__(self, title):
        super().__init__()
        self.setStyleSheet("background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.16); border-radius: 18px;")
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(4)
        label = make_label(title, metricLabel=True)
        label.setStyleSheet("color: rgba(255,255,255,0.72);")
        self.value = QtWidgets.QLabel("-")
        self.value.setStyleSheet("color: white; font-size: 15px; font-weight: 800;")
        layout.addWidget(label)
        layout.addWidget(self.value)


class SummaryCard(QtWidgets.QFrame):
    def __init__(self, title, tone):
        super().__init__()
        tones = {
            "soft": "background: #f9f8f8; border: 1px solid rgba(20,19,26,0.06); border-radius: 24px;",
            "coral": "background: #edb9b6; border-radius: 24px;",
            "dark": "background: #14131a; border-radius: 24px;",
        }
        self.setStyleSheet(tones[tone])
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        eyebrow = make_label(title, eyebrow=True)
        if tone == "dark":
            eyebrow.setStyleSheet("color: rgba(255,255,255,0.68); font-size: 11px; font-weight: 700;")
        self.value = QtWidgets.QLabel("0")
        self.value.setStyleSheet("font-size: 32px; font-weight: 800; color: {0};".format("white" if tone == "dark" else "#14131a"))
        self.note = QtWidgets.QLabel("-")
        self.note.setWordWrap(True)
        self.note.setStyleSheet("color: {0};".format("rgba(255,255,255,0.72)" if tone == "dark" else "#5b5860"))
        layout.addWidget(eyebrow)
        layout.addWidget(self.value)
        layout.addWidget(self.note)
        layout.addStretch(1)


class LineProgress(QtWidgets.QWidget):
    def __init__(self, label_text):
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        self.label = QtWidgets.QLabel(label_text)
        self.label.setStyleSheet("color: rgba(255,255,255,0.78); min-width: 140px;")
        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet(
            "QProgressBar {background: rgba(255,255,255,0.20); border: none; border-radius: 6px; height: 10px;}"
            "QProgressBar::chunk {background: white; border-radius: 6px;}"
        )
        layout.addWidget(self.label)
        layout.addWidget(self.progress, 1)


class RowCard(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: #fbfbfb; border: 1px solid rgba(20,19,26,0.08); border-radius: 18px;")
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)
        self.left = QtWidgets.QVBoxLayout()
        self.left.setSpacing(4)
        self.title = QtWidgets.QLabel("-")
        self.title.setStyleSheet("font-size: 15px; font-weight: 800;")
        self.subtitle = QtWidgets.QLabel("-")
        self.subtitle.setStyleSheet("color: #7f7b85;")
        self.left.addWidget(self.title)
        self.left.addWidget(self.subtitle)
        layout.addLayout(self.left, 1)
        self.badge = StatusBadge("-", "light")
        layout.addWidget(self.badge)

    def set_data(self, title, subtitle, badge, badge_kind="light"):
        self.title.setText(title)
        self.subtitle.setText(subtitle)
        self.badge.setText(badge)
        self.badge.set_kind(badge_kind)


class SectionCard(QtWidgets.QFrame):
    def __init__(self, eyebrow, title):
        super().__init__()
        self.setStyleSheet("background: rgba(255,255,255,0.95); border: 1px solid rgba(20,19,26,0.08); border-radius: 24px;")
        self.outer = QtWidgets.QVBoxLayout(self)
        self.outer.setContentsMargins(20, 20, 20, 20)
        self.outer.setSpacing(16)
        self.outer.addWidget(make_label(eyebrow, eyebrow=True))
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("font-size: 20px; font-weight: 800;")
        self.outer.addWidget(title_label)


class WatcherQtWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tongzhi Watcher")
        self.resize(1360, 900)
        self.setMinimumSize(1180, 780)

        self.controller = WatcherController()
        self.data = config.load_config()
        self.editing_index = -1
        self.type_labels = channels.channel_type_labels()
        self.type_values = list(self.type_labels.keys())
        self.nav_buttons = {}

        self._build_ui()
        self._load_config_to_form()
        self._refresh_all()

        self.refresh_timer = QtCore.QTimer(self)
        self.refresh_timer.timeout.connect(self._refresh_all)
        self.refresh_timer.start(2000)

    def _build_ui(self):
        root = QtWidgets.QWidget()
        root.setObjectName("RootFrame")
        self.setCentralWidget(root)

        outer = QtWidgets.QHBoxLayout(root)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(20)

        sidebar = QtWidgets.QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(250)
        outer.addWidget(sidebar)

        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 18, 18, 18)
        sidebar_layout.setSpacing(14)

        brand_row = QtWidgets.QHBoxLayout()
        brand_mark = QtWidgets.QLabel("T")
        brand_mark.setObjectName("BrandMark")
        brand_mark.setFixedSize(52, 52)
        brand_mark.setAlignment(QtCore.Qt.AlignCenter)
        brand_col = QtWidgets.QVBoxLayout()
        brand_col.addWidget(make_label("Tongzhi", eyebrow=True))
        brand_title = QtWidgets.QLabel("Watcher")
        brand_title.setStyleSheet("font-size: 28px; font-weight: 800;")
        brand_col.addWidget(brand_title)
        brand_row.addWidget(brand_mark)
        brand_row.addLayout(brand_col)
        sidebar_layout.addLayout(brand_row)

        for key, title in (("overview", "Overview"), ("channels", "Channels"), ("history", "History"), ("logs", "Logs")):
            btn = NavButton(key, title)
            btn.clicked_page.connect(self._switch_page)
            sidebar_layout.addWidget(btn)
            self.nav_buttons[key] = btn

        sidebar_layout.addStretch(1)

        main_surface = QtWidgets.QFrame()
        main_surface.setObjectName("MainSurface")
        outer.addWidget(main_surface, 1)

        main_layout = QtWidgets.QVBoxLayout(main_surface)
        main_layout.setContentsMargins(22, 22, 22, 22)
        main_layout.setSpacing(18)

        topbar = QtWidgets.QHBoxLayout()
        left_col = QtWidgets.QVBoxLayout()
        left_col.addWidget(make_label("Desktop Control Panel", eyebrow=True))
        title = make_label("Realtime Render Watcher", title=True)
        left_col.addWidget(title)
        topbar.addLayout(left_col)
        topbar.addStretch(1)

        for text, handler, primary in (
            ("Test Send", self._test_send, False),
            ("Open Data Dir", self._open_data_dir, False),
            ("Start Watcher", self._toggle_watcher, True),
        ):
            btn = QtWidgets.QPushButton(text)
            if primary:
                btn.setProperty("primary", True)
            btn.clicked.connect(handler)
            topbar.addWidget(btn)
        main_layout.addLayout(topbar)

        self.pages = QtWidgets.QStackedWidget()
        main_layout.addWidget(self.pages, 1)
        self.pages.addWidget(self._build_overview_page())
        self.pages.addWidget(self._build_channels_page())
        self.pages.addWidget(self._build_history_page())
        self.pages.addWidget(self._build_logs_page())
        self._switch_page("overview")

    def _build_overview_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setSpacing(18)

        top = QtWidgets.QHBoxLayout()
        top.setSpacing(18)

        hero = QtWidgets.QFrame()
        hero.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #249782, stop:1 #1e7f6d); border-radius: 28px;")
        hero_layout = QtWidgets.QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 24, 24, 24)
        hero_layout.setSpacing(18)

        head = QtWidgets.QHBoxLayout()
        head_left = QtWidgets.QVBoxLayout()
        head_left.addWidget(make_label("Current Session", heroSub=True))
        self.hero_project = make_label("No active render", heroTitle=True)
        head_left.addWidget(self.hero_project)
        head.addLayout(head_left)
        head.addStretch(1)
        self.hero_status = StatusBadge("Idle", "green")
        head.addWidget(self.hero_status)
        hero_layout.addLayout(head)

        metric_grid = QtWidgets.QGridLayout()
        metric_grid.setSpacing(12)
        self.metric_cards = {}
        for idx, (title, key) in enumerate((("Machine", "machine"), ("Render Mode", "mode"), ("Timeout", "timeout"), ("Runtime State", "runtime"))):
            card = MetricCard(title)
            self.metric_cards[key] = card
            metric_grid.addWidget(card, idx // 2, idx % 2)
        hero_layout.addLayout(metric_grid)

        self.signal_rows = [LineProgress(text) for text in ("Plugin heartbeat", "Watcher status", "Output sync")]
        for row in self.signal_rows:
            hero_layout.addWidget(row)
        top.addWidget(hero, 3)

        summary_col = QtWidgets.QVBoxLayout()
        summary_col.setSpacing(16)
        self.summary_cards = {
            "channels": SummaryCard("Enabled Channels", "soft"),
            "last_notice": SummaryCard("Last Notification", "coral"),
            "autostart": SummaryCard("Autostart", "dark"),
        }
        for key in ("channels", "last_notice", "autostart"):
            summary_col.addWidget(self.summary_cards[key])
        top.addLayout(summary_col, 2)
        layout.addLayout(top)

        middle = QtWidgets.QHBoxLayout()
        middle.setSpacing(18)
        self.health_section = SectionCard("Health", "Watcher Runtime")
        self.health_rows = [RowCard() for _ in range(3)]
        for row in self.health_rows:
            self.health_section.outer.addWidget(row)
        middle.addWidget(self.health_section, 1)

        self.channel_section = SectionCard("Channels", "Notification Routing")
        self.channel_rows = [RowCard() for _ in range(3)]
        for row in self.channel_rows:
            self.channel_section.outer.addWidget(row)
        middle.addWidget(self.channel_section, 1)
        layout.addLayout(middle)

        bottom = QtWidgets.QHBoxLayout()
        bottom.setSpacing(18)

        self.timeline_section = SectionCard("Events", "Recent History")
        self.timeline_box = QtWidgets.QPlainTextEdit()
        self.timeline_box.setReadOnly(True)
        self.timeline_box.setMinimumHeight(240)
        self.timeline_section.outer.addWidget(self.timeline_box)
        bottom.addWidget(self.timeline_section, 1)

        self.logs_section = SectionCard("Logs", "Live Diagnostic Feed")
        self.log_preview = QtWidgets.QPlainTextEdit()
        self.log_preview.setReadOnly(True)
        self.log_preview.setMinimumHeight(240)
        self.log_preview.setStyleSheet(
            "QPlainTextEdit {background: #17161f; color: #f3f2f7; border: none; border-radius: 20px; padding: 16px; font-family: Consolas, monospace;}"
        )
        self.logs_section.outer.addWidget(self.log_preview)
        bottom.addWidget(self.logs_section, 1)
        layout.addLayout(bottom)
        return page

    def _build_channels_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(page)
        layout.setSpacing(18)

        left = SectionCard("Base Settings", "Watcher Configuration")
        self.machine_edit = QtWidgets.QLineEdit()
        self.timeout_spin = QtWidgets.QSpinBox()
        self.timeout_spin.setRange(1, 999999)
        self.poll_spin = QtWidgets.QSpinBox()
        self.poll_spin.setRange(1, 3600)
        self.autostart_check = QtWidgets.QCheckBox("Start watcher UI with Windows")
        form = QtWidgets.QFormLayout()
        form.addRow("Machine name", self.machine_edit)
        form.addRow("Timeout seconds", self.timeout_spin)
        form.addRow("Watcher poll seconds", self.poll_spin)
        form.addRow("", self.autostart_check)
        left.outer.addLayout(form)
        path_text = QtWidgets.QPlainTextEdit()
        path_text.setReadOnly(True)
        path_text.setMaximumHeight(130)
        path_text.setPlainText(
            "Config: {0}\nRuntime: {1}\nPlugin log: {2}\nWatcher log: {3}".format(
                config.get_config_path(),
                config.get_runtime_state_path(),
                config.get_plugin_log_path(),
                config.get_watcher_log_path(),
            )
        )
        left.outer.addWidget(path_text)
        save_btn = QtWidgets.QPushButton("Save Config")
        save_btn.setProperty("primary", True)
        save_btn.clicked.connect(self._save_config)
        left.outer.addWidget(save_btn)
        layout.addWidget(left, 1)

        right = SectionCard("Channels", "Channel Editor")
        split = QtWidgets.QHBoxLayout()
        self.channel_list = QtWidgets.QListWidget()
        self.channel_list.currentRowChanged.connect(self._on_channel_selected)
        split.addWidget(self.channel_list, 1)

        editor = QtWidgets.QWidget()
        editor_form = QtWidgets.QFormLayout(editor)
        self.channel_name_edit = QtWidgets.QLineEdit()
        self.channel_type_combo = QtWidgets.QComboBox()
        for key in self.type_values:
            self.channel_type_combo.addItem(self.type_labels[key], key)
        self.channel_endpoint_edit = QtWidgets.QLineEdit()
        self.channel_enabled_check = QtWidgets.QCheckBox("Enable this channel")
        editor_form.addRow("Channel name", self.channel_name_edit)
        editor_form.addRow("Channel type", self.channel_type_combo)
        editor_form.addRow("Webhook / SendKey", self.channel_endpoint_edit)
        editor_form.addRow("", self.channel_enabled_check)
        btn_row = QtWidgets.QHBoxLayout()
        for text, callback in (("New", self._new_channel), ("Save Channel", self._save_channel), ("Delete", self._delete_channel)):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(callback)
            btn_row.addWidget(btn)
        editor_form.addRow(btn_row)
        split.addWidget(editor, 2)
        right.outer.addLayout(split)
        layout.addWidget(right, 2)
        return page

    def _build_history_page(self):
        page = SectionCard("Recent Notifications", "History")
        self.history_text = QtWidgets.QPlainTextEdit()
        self.history_text.setReadOnly(True)
        page.outer.addWidget(self.history_text)
        return page

    def _build_logs_page(self):
        page = SectionCard("Diagnostics", "Logs")
        toolbar = QtWidgets.QHBoxLayout()
        toolbar.addStretch(1)
        for text, callback in (("Reload", self._refresh_logs_text), ("Open Plugin Log", lambda: self._open_path(config.get_plugin_log_path())), ("Open Watcher Log", lambda: self._open_path(config.get_watcher_log_path()))):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(callback)
            toolbar.addWidget(btn)
        page.outer.addLayout(toolbar)
        self.logs_text = QtWidgets.QPlainTextEdit()
        self.logs_text.setReadOnly(True)
        page.outer.addWidget(self.logs_text)
        return page

    def _switch_page(self, name):
        mapping = {"overview": 0, "channels": 1, "history": 2, "logs": 3}
        self.pages.setCurrentIndex(mapping[name])
        for key, btn in self.nav_buttons.items():
            btn.set_active(key == name)

    def _load_config_to_form(self):
        self.machine_edit.setText(self.data.get("machine_name", ""))
        self.timeout_spin.setValue(int(self.data.get("timeout_seconds", constants.DEFAULT_TIMEOUT_SECONDS)))
        watcher = self.data.get("watcher", {})
        self.poll_spin.setValue(int(watcher.get("poll_interval_seconds", constants.WATCHER_POLL_INTERVAL_SECONDS)))
        self.autostart_check.setChecked(bool(watcher.get("start_with_windows", False) or autostart.is_enabled()))
        self._refresh_channel_editor()

    def _refresh_channel_editor(self):
        self.channel_list.clear()
        for channel in self.data.get("channels", []):
            state = "Enabled" if channel.get("enabled", True) else "Disabled"
            self.channel_list.addItem("{0} | {1} | {2}".format(channel.get("name", "Unnamed"), self.type_labels.get(channel.get("type"), "Unknown"), state))
        self._new_channel()

    def _new_channel(self):
        self.editing_index = -1
        self.channel_name_edit.clear()
        self.channel_type_combo.setCurrentIndex(0)
        self.channel_endpoint_edit.clear()
        self.channel_enabled_check.setChecked(True)
        self.channel_list.clearSelection()

    def _on_channel_selected(self, row):
        if row < 0 or row >= len(self.data.get("channels", [])):
            return
        self.editing_index = row
        channel = self.data["channels"][row]
        self.channel_name_edit.setText(channel.get("name", ""))
        combo_index = max(0, self.channel_type_combo.findData(channel.get("type", self.type_values[0])))
        self.channel_type_combo.setCurrentIndex(combo_index)
        self.channel_endpoint_edit.setText(channel.get("endpoint", ""))
        self.channel_enabled_check.setChecked(channel.get("enabled", True))

    def _save_channel(self):
        item = {
            "name": self.channel_name_edit.text().strip(),
            "type": self.channel_type_combo.currentData(),
            "endpoint": self.channel_endpoint_edit.text().strip(),
            "enabled": self.channel_enabled_check.isChecked(),
        }
        if not item["name"]:
            QtWidgets.QMessageBox.warning(self, "Error", "Channel name is required.")
            return
        if not item["endpoint"]:
            QtWidgets.QMessageBox.warning(self, "Error", "Webhook endpoint or SendKey is required.")
            return
        if self.editing_index < 0 or self.editing_index >= len(self.data["channels"]):
            self.data["channels"].append(item)
        else:
            self.data["channels"][self.editing_index] = item
        self._refresh_channel_editor()

    def _delete_channel(self):
        if self.editing_index < 0 or self.editing_index >= len(self.data.get("channels", [])):
            return
        del self.data["channels"][self.editing_index]
        self._refresh_channel_editor()

    def _collect_config(self):
        return {
            "machine_name": self.machine_edit.text().strip(),
            "timeout_seconds": self.timeout_spin.value(),
            "channels": self.data.get("channels", []),
            "watcher": {
                "poll_interval_seconds": self.poll_spin.value(),
                "start_with_windows": self.autostart_check.isChecked(),
            },
        }

    def _save_config(self):
        payload = self._collect_config()
        valid, message = config.validate_config(payload)
        if not valid:
            QtWidgets.QMessageBox.warning(self, "Config error", message)
            return
        config.save_config(payload)
        self.data = config.load_config()
        if self.autostart_check.isChecked():
            autostart.enable(os.path.abspath(__file__))
        else:
            autostart.disable()
        self.statusBar().showMessage("Config saved", 3000)
        self._refresh_all()

    def _toggle_watcher(self):
        if self.controller.is_running():
            self.controller.stop()
            self.statusBar().showMessage("Watcher stopped", 3000)
        else:
            self.controller.start()
            self.statusBar().showMessage("Watcher started", 3000)
        self._refresh_runtime_summary()

    def _test_send(self):
        ok, error = send_test()
        if ok:
            QtWidgets.QMessageBox.information(self, "Done", "Test message sent.")
        else:
            QtWidgets.QMessageBox.warning(self, "Test failed", error)
        self._refresh_all()

    def _open_data_dir(self):
        self._open_path(config.get_data_dir())

    def _open_path(self, path):
        try:
            os.startfile(path)
        except Exception:
            try:
                subprocess.Popen(["explorer", path])
            except Exception as exc:
                QtWidgets.QMessageBox.warning(self, "Open failed", str(exc))

    def _refresh_all(self):
        self.data = config.load_config()
        self._refresh_runtime_summary()
        self._refresh_history_text()
        self._refresh_logs_text()
        self._refresh_overview_rows()

    def _refresh_runtime_summary(self):
        state = load_state()
        running = self.controller.is_running()
        self.hero_project.setText(state.get("project_name") or "No active render")
        self.hero_status.setText("Watching" if running else "Stopped")
        self.metric_cards["machine"].value.setText(state.get("machine_name") or self.data.get("machine_name", "-"))
        self.metric_cards["mode"].value.setText(state.get("render_mode") or "Idle")
        self.metric_cards["timeout"].value.setText(str(state.get("timeout_seconds", self.data.get("timeout_seconds", 0))) + "s")
        self.metric_cards["runtime"].value.setText("runtime_state.json")

        self.signal_rows[0].progress.setValue(92 if state.get("last_heartbeat_at") else 12)
        self.signal_rows[1].progress.setValue(88 if running else 24)
        self.signal_rows[2].progress.setValue(72 if state.get("output_path") else 18)

        history = load_history()
        enabled_channels = len([item for item in self.data.get("channels", []) if item.get("enabled", True)])
        self.summary_cards["channels"].value.setText(str(enabled_channels))
        self.summary_cards["channels"].note.setText("Feishu / ServerChan / Webhook")

        if history:
            latest = history[-1]
            time_text = latest.get("time", "")
            self.summary_cards["last_notice"].value.setText(time_text[-8:-3] if len(time_text) >= 5 else "--:--")
            self.summary_cards["last_notice"].note.setText(latest.get("event_type", "notification"))
        else:
            self.summary_cards["last_notice"].value.setText("--:--")
            self.summary_cards["last_notice"].note.setText("No notification yet")

        self.summary_cards["autostart"].value.setText("On" if autostart.is_enabled() else "Off")
        self.summary_cards["autostart"].note.setText("Tray + Windows startup enabled" if autostart.is_enabled() else "Manual start")

    def _refresh_overview_rows(self):
        state = load_state()
        rows = [
            ("Watcher Loop", "{0}s polling interval".format(self.controller.poll_interval_seconds()), "running" if self.controller.is_running() else "stopped", "light"),
            ("Tray Session", "Qt tray comes after shell migration", "planned", "dark"),
            ("Plugin Link", "runtime_state heartbeat updating" if state.get("last_heartbeat_at") else "waiting for data", "linked" if state.get("last_heartbeat_at") else "idle", "light"),
        ]
        for widget, data in zip(self.health_rows, rows):
            widget.set_data(*data)

        channel_rows = self.data.get("channels", [])[:3]
        while len(channel_rows) < 3:
            channel_rows.append({"name": "Unused slot", "enabled": False, "type": ""})
        for widget, channel in zip(self.channel_rows, channel_rows):
            widget.set_data(
                channel.get("name", "Unnamed"),
                self.type_labels.get(channel.get("type"), "Notification channel"),
                "enabled" if channel.get("enabled", True) else "disabled",
                "light" if channel.get("enabled", True) else "dark",
            )

    def _refresh_history_text(self):
        history = load_history()
        if not history:
            self.history_text.setPlainText("No notification history yet.")
            self.timeline_box.setPlainText("No notification history yet.")
            return
        lines = []
        preview = []
        for item in reversed(history[-20:]):
            lines.append(
                "[{0}] {1}\nProject: {2}\nSuccess: {3}\nMessage: {4}\n".format(
                    item.get("time", ""),
                    item.get("event_type", ""),
                    item.get("project_name", ""),
                    item.get("success", False),
                    item.get("message", ""),
                )
            )
            preview.append("[{0}] {1} | {2}".format(item.get("time", "")[-8:], item.get("event_type", ""), item.get("project_name", "")))
        self.history_text.setPlainText("\n".join(lines))
        self.timeline_box.setPlainText("\n".join(preview[:8]))

    def _refresh_logs_text(self):
        sections = []
        preview_lines = []
        for label, path in (("Plugin log", config.get_plugin_log_path()), ("Watcher log", config.get_watcher_log_path())):
            sections.append("== {0} ==\n".format(label))
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as handle:
                        content = handle.read()
                except Exception as exc:
                    content = "Failed to read log: {0}\n".format(exc)
                sections.append(content)
                lines = [line for line in content.splitlines() if line.strip()]
                preview_lines.extend(lines[-4:])
            else:
                sections.append("Log file does not exist yet.\n")
            sections.append("\n")
        self.logs_text.setPlainText("".join(sections))
        self.log_preview.setPlainText("\n".join(preview_lines[-10:]) or "No logs yet.")


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Tongzhi Watcher")
    app.setStyleSheet(APP_STYLE)
    window = WatcherQtWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
