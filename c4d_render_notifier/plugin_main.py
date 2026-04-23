import c4d

import config
import constants
import logger
import monitor


class RenderMonitorMessage(c4d.plugins.MessageData):
    def GetTimer(self):
        return constants.MONITOR_INTERVAL_MS

    def CoreMessage(self, mid, bc):
        if mid == c4d.MSG_TIMER:
            monitor.monitor_tick()
        return True


class ShowStatusCommand(c4d.plugins.CommandData):
    def Execute(self, doc):
        current = config.load_config()
        enabled = [item for item in current.get("channels", []) if item.get("enabled", True)]
        message = (
            "Tongzhi Render Notifier is loaded.\n\n"
            "Config file: {0}\n"
            "Log file: {1}\n"
            "Runtime state: {2}\n"
            "Machine name: {3}\n"
            "Enabled channels: {4}\n\n"
            "This plugin only writes render state now.\n"
            "Please use the external configurator and watcher."
        ).format(
            config.get_config_path(),
            logger.get_log_path(),
            config.get_runtime_state_path(),
            current.get("machine_name", ""),
            len(enabled),
        )
        c4d.gui.MessageDialog(message)
        return True


def register():
    logger.log("plugin register invoked")
    ok_command = c4d.plugins.RegisterCommandPlugin(
        id=constants.COMMAND_PLUGIN_ID,
        str="Tongzhi Render Notifier",
        info=0,
        icon=None,
        help="Show notifier status and config path.",
        dat=ShowStatusCommand(),
    )
    ok_message = c4d.plugins.RegisterMessagePlugin(
        id=constants.MESSAGE_PLUGIN_ID,
        str="Tongzhi Render Notifier Background",
        info=c4d.PLUGINFLAG_HIDEPLUGINMENU,
        dat=RenderMonitorMessage(),
    )
    logger.log("plugin register result: command={0}, message={1}".format(ok_command, ok_message))
    return bool(ok_command and ok_message)
