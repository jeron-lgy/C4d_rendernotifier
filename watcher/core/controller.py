import threading
import time

from .detector import WatcherDetector
from .logger import log


class WatcherController(object):
    def __init__(self):
        self._thread = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._running = False
        self._detector = WatcherDetector()

    def start(self):
        with self._lock:
            if self._running:
                return False
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run_loop, name="TongzhiWatcher", daemon=True)
            self._thread.start()
            self._running = True
            log("watcher controller started")
            return True

    def stop(self):
        with self._lock:
            if not self._running:
                return False
            self._stop_event.set()
            self._running = False
            log("watcher controller stop requested")
            return True

    def is_running(self):
        with self._lock:
            return self._running

    def poll_interval_seconds(self):
        return self._detector.poll_interval_seconds()

    def tick_once(self):
        self._detector.tick()

    def _run_loop(self):
        while not self._stop_event.is_set():
            try:
                self._detector.tick()
            except Exception as exc:
                log("watcher loop error: {0}".format(exc))
            self._stop_event.wait(self._detector.poll_interval_seconds())
        log("watcher controller stopped")

