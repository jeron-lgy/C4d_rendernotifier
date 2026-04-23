import threading

from .logger import log


class TrayManager(object):
    def __init__(self, app):
        self.app = app
        self._icon = None
        self._thread = None
        self._enabled = False
        self._last_error = ""

    def start(self):
        if self._enabled:
            return True
        try:
            import pystray
            from PIL import Image, ImageDraw
        except Exception as exc:
            self._last_error = str(exc)
            log("tray unavailable: {0}".format(exc))
            return False

        def create_image():
            image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.rounded_rectangle((8, 8, 56, 56), radius=14, fill=(38, 98, 255, 255))
            draw.rectangle((28, 16, 36, 48), fill=(255, 255, 255, 255))
            draw.rectangle((18, 28, 46, 36), fill=(255, 255, 255, 255))
            return image

        def on_show(icon, item):
            self.app.root.after(0, self.app.show_from_tray)

        def on_toggle(icon, item):
            self.app.root.after(0, self.app.toggle_watcher_from_tray)

        def on_test(icon, item):
            self.app.root.after(0, self.app._test_send)

        def on_open_dir(icon, item):
            self.app.root.after(0, self.app._open_data_dir)

        def on_exit(icon, item):
            self.app.root.after(0, self.app.exit_application)

        menu = pystray.Menu(
            pystray.MenuItem("Open Panel", on_show),
            pystray.MenuItem("Start / Stop Watcher", on_toggle),
            pystray.MenuItem("Test Send", on_test),
            pystray.MenuItem("Open Data Dir", on_open_dir),
            pystray.MenuItem("Exit", on_exit),
        )

        self._icon = pystray.Icon("tongzhi_watcher", create_image(), "Tongzhi Watcher", menu)
        self._thread = threading.Thread(target=self._run_icon, name="TongzhiTray", daemon=True)
        self._thread.start()
        self._enabled = True
        self._last_error = ""
        log("tray started")
        return True

    def _run_icon(self):
        try:
            self._icon.run()
        except Exception as exc:
            log("tray stopped with error: {0}".format(exc))

    def stop(self):
        if self._icon is not None:
            try:
                self._icon.stop()
            except Exception as exc:
                log("tray stop error: {0}".format(exc))
        self._enabled = False

    def is_enabled(self):
        return self._enabled

    def last_error(self):
        return self._last_error
