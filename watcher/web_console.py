import json
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, "frozen", False):
    RESOURCE_ROOT = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    WEB_DIR = os.path.join(RESOURCE_ROOT, "web")
    PLUGIN_SHARED_DIR = os.path.join(RESOURCE_ROOT, "c4d_render_notifier")
else:
    RESOURCE_ROOT = os.path.dirname(CURRENT_DIR)
    WEB_DIR = os.path.join(CURRENT_DIR, "web")
    PLUGIN_SHARED_DIR = os.path.join(RESOURCE_ROOT, "c4d_render_notifier")

if PLUGIN_SHARED_DIR not in sys.path:
    sys.path.insert(0, PLUGIN_SHARED_DIR)

import config

from core.logger import log
from core.service import WatcherService


HOST = "127.0.0.1"
PORT = 37673
APP_URL = "http://{0}:{1}/".format(HOST, PORT)


class WebConsoleHandler(BaseHTTPRequestHandler):
    service = None
    script_path = None

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, file_path, content_type="text/html; charset=utf-8"):
        if not os.path.exists(file_path):
            self.send_error(404)
            return
        with open(file_path, "rb") as handle:
            body = handle.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        if not raw:
            return {}
        return json.loads(raw)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path in ("/", "/index.html"):
            return self._send_file(os.path.join(WEB_DIR, "index.html"))
        if path == "/styles.css":
            return self._send_file(os.path.join(WEB_DIR, "styles.css"), "text/css; charset=utf-8")
        if path == "/app.js":
            return self._send_file(os.path.join(WEB_DIR, "app.js"), "application/javascript; charset=utf-8")
        if path == "/api/status":
            return self._send_json(self.service.get_status_payload())
        if path == "/api/config":
            return self._send_json(self.service.get_config_payload())
        if path == "/api/notification-defaults":
            return self._send_json(self.service.get_notification_defaults())
        if path == "/api/history":
            return self._send_json(self.service.get_history_payload())
        if path == "/api/logs":
            return self._send_json(self.service.get_logs_payload())
        self.send_error(404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/api/config":
            payload = self._read_json_body()
            ok, message = self.service.save_config_payload(payload, script_path=self.script_path)
            return self._send_json({"ok": ok, "message": message}, status=200 if ok else 400)
        if path == "/api/test-send":
            ok, message = self.service.test_send()
            return self._send_json({"ok": ok, "message": message}, status=200 if ok else 400)
        if path == "/api/watcher/start":
            ok = self.service.start_watcher()
            return self._send_json({"ok": ok, "running": self.service.controller.is_running()})
        if path == "/api/watcher/stop":
            ok = self.service.stop_watcher()
            return self._send_json({"ok": ok, "running": self.service.controller.is_running()})
        if path == "/api/watcher/tick":
            self.service.tick_once()
            return self._send_json({"ok": True})
        self.send_error(404)

    def log_message(self, format, *args):
        return


class WebConsoleTray(object):
    def __init__(self, service, server):
        self.service = service
        self.server = server
        self.icon = None
        self.enabled = False
        self.pystray = None
        self.Image = None
        self.ImageDraw = None

    def _create_image(self, running):
        image = self.Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = self.ImageDraw.Draw(image)
        fill = (36, 151, 130, 255) if running else (237, 185, 182, 255)
        accent = (255, 255, 255, 255) if running else (20, 19, 26, 255)
        draw.rounded_rectangle((8, 8, 56, 56), radius=14, fill=fill)
        draw.rectangle((28, 16, 36, 48), fill=accent)
        draw.rectangle((18, 28, 46, 36), fill=accent)
        return image

    def _refresh_icon_state(self):
        if self.icon is None:
            return
        running = self.service.controller.is_running()
        self.icon.icon = self._create_image(running)
        self.icon.title = "Tongzhi Watcher ({0})".format("running" if running else "stopped")
        self.icon.update_menu()

    def start(self):
        try:
            import pystray
            from PIL import Image, ImageDraw
        except Exception as exc:
            log("web console tray unavailable: {0}".format(exc))
            return False
        self.pystray = pystray
        self.Image = Image
        self.ImageDraw = ImageDraw

        def open_console(icon, item):
            webbrowser.open(APP_URL)

        def start_watcher(icon, item):
            self.service.start_watcher()
            self._refresh_icon_state()
            log("tray requested watcher start")

        def stop_watcher(icon, item):
            self.service.stop_watcher()
            self._refresh_icon_state()
            log("tray requested watcher stop")

        def test_send(icon, item):
            ok, message = self.service.test_send()
            log("tray test send result: ok={0}, message={1}".format(ok, message))

        def exit_all(icon, item):
            try:
                self.service.stop_watcher()
            finally:
                try:
                    self.server.shutdown()
                except Exception:
                    pass
                try:
                    icon.stop()
                except Exception:
                    pass

        menu = self.pystray.Menu(
            self.pystray.MenuItem("Open Console", open_console),
            self.pystray.MenuItem(
                "Start Watcher",
                start_watcher,
                enabled=lambda item: not self.service.controller.is_running(),
            ),
            self.pystray.MenuItem(
                "Stop Watcher",
                stop_watcher,
                enabled=lambda item: self.service.controller.is_running(),
            ),
            self.pystray.MenuItem("Test Send", test_send),
            self.pystray.MenuItem("Exit", exit_all),
        )
        self.icon = self.pystray.Icon(
            "tongzhi_web_console",
            self._create_image(self.service.controller.is_running()),
            "Tongzhi Watcher",
            menu,
        )
        thread = threading.Thread(target=self.icon.run, name="TongzhiWebTray", daemon=True)
        thread.start()
        self.enabled = True
        log("web console tray started")
        return True


def main(open_browser=True):
    config.ensure_data_dir()
    service = WatcherService()
    WebConsoleHandler.service = service
    WebConsoleHandler.script_path = os.path.abspath(__file__)
    server = ThreadingHTTPServer((HOST, PORT), WebConsoleHandler)
    tray = WebConsoleTray(service, server)
    tray.start()
    service.start_watcher()
    tray._refresh_icon_state()
    log("web console started: {0}".format(APP_URL))
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(APP_URL)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("web console stopped by keyboard interrupt")
    finally:
        try:
            if tray.icon is not None:
                tray.icon.stop()
        except Exception:
            pass
        service.stop_watcher()
        server.server_close()


if __name__ == "__main__":
    main()
