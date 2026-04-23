import os
import sys


PLUGIN_DIR = os.path.dirname(__file__)
if PLUGIN_DIR not in sys.path:
    sys.path.insert(0, PLUGIN_DIR)

from plugin_main import register


def main():
    register()


if __name__ == "__main__":
    main()
