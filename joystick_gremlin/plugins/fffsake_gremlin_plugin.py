import inspect
import os.path
import sys

import gremlin
from gremlin.user_plugin import *
import gremlin.util

import fffsake


mode = ModeVariable("Mode", "The mode to use for this mapping")
ffb_toggle = PhysicalInputVariable(
    "FFB Toggle",
    "Button to toggle Force Feedback on/off. Can be on any device",
    [gremlin.common.InputType.JoystickButton],
)
decorator_ffb_toggle = ffb_toggle.create_decorator(mode.value)


def _process_registry_value(self, value):
    return str(value)


SelectionVariable._process_registry_value = _process_registry_value


# Doesn't work if the user has multiple devices with the
# same name - this is unlikely to need support.
device_selector = SelectionVariable(
    "FF Device",
    "Which device to send force feedback commands to.",
    [d.name for d in fffsake.DetectFfbDevices() if not d.is_virtual],
    is_optional=True,
)


def UpdateDeviceSelector(selector):
    selector.options = [d.name for d in fffsake.DetectFfbDevices() if not d.is_virtual]


@decorator_ffb_toggle.button(ffb_toggle.input_id)
def ffb_toggle_handler(event):
    # Button press generates two events; act only on one of them.
    if event.is_pressed:
        if fffsake.IsFffsakeActive():
            gremlin.util.log("Stopping fffsake")
            fffsake.FffsakeCleanup()
        else:
            gremlin.util.log("FFB Device selected: %s" % device_selector.value)
            for d in fffsake.DetectFfbDevices():
                if not d.is_virtual and d.name == device_selector.value:
                    fffsake.RegisterFffsakeReducer(d.guid)
                    gremlin.util.log("FFFSake reducer engine active")
                    break
            else:
                gremlin.util.log(
                    "Device (no longer?) present: %s" % device_selector.value
                )
    # There's currently a bug in the Periodic decorator, so this device selector
    # update happens here - not ideal.
    UpdateDeviceSelector(device_selector)
