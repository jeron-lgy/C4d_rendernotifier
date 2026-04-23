import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PLUGIN_SHARED_DIR = os.path.join(BASE_DIR, "c4d_render_notifier")
if PLUGIN_SHARED_DIR not in sys.path:
    sys.path.insert(0, PLUGIN_SHARED_DIR)

from core.controller import WatcherController
from core.logger import log


def main():
    log("watcher starting")
    controller = WatcherController()
    controller.start()
    try:
        while True:
            # Keep the process alive while the background thread runs.
            controller._stop_event.wait(3600)
    except KeyboardInterrupt:
        log("watcher stopped by keyboard interrupt")
        controller.stop()


if __name__ == "__main__":
    main()

