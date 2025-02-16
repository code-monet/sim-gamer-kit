""" © 2025 Code Monet <code.monet@proton.me>

Joystick Gremlin plugin for FFFSake.
"""

import inspect
import os.path
import sys
import threading
import time

import gremlin.common
import gremlin.event_handler
from gremlin.user_plugin import *
import gremlin.util

current_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
while True:
    head, tail = os.path.split(current_path)
    if tail == "joystick_gremlin":
        sys.path.append(head)
        break
    current_path = head

from fffsake.x86 import fffsake


mode = ModeVariable("Mode", "The mode to use for this mapping")
ffb_toggle = PhysicalInputVariable(
    "FFFSake Toggle",
    "Button to toggle Force Feedback on/off. Can be on any device",
    [gremlin.common.InputType.JoystickButton],
)
decorator_ffb_toggle = ffb_toggle.create_decorator(mode.value)


def _process_registry_value(self, value):
    return str(value)


SelectionVariable._process_registry_value = _process_registry_value


# Doesn't work if the user has multiple devices with the
# same name - this is unlikely to need support.
# TODO: This list only populates at Gremlin launch, and after each "Activate".
try:
    device_selector = SelectionVariable(
        "FF Device",
        "Which device to send force feedback commands to.",
        [d.name for d in fffsake.DetectFfbDevices() if not d.is_virtual],
        is_optional=True,
    )
except AssertionError:
    # Our best guess as to why this might happen:
    gremlin.util.display_error(
        "FFFSake plugins says: No FFB-capable devices;"
        " please connect/power on your FFB device and retry."
    )


# TODO: Is this function thread safe?
def StartUp():
    gremlin.util.log("FFB Device selected: %s" % device_selector.value)
    for d in fffsake.DetectFfbDevices():
        if not d.is_virtual and d.name == device_selector.value:
            fffsake.RegisterFffsakeReducer(d.guid)
            gremlin.util.log("FFFSake reducer engine active")
            break
    else:
        gremlin.util.display_error(
            "Device (no longer?) present: %s" % device_selector.value
        )


def ShutDown():
    fffsake.FffsakeCleanup()
    gremlin.util.log("FFFSake disabled")


class ActivationThread(threading.Thread):
    """Thread that activates/deactivates fffsake with Gremlin activation.
    
    Thread exits when the main thread exits.
    """

    def __init__(self):
        super().__init__()
        self.user_ffsake_enable = threading.Event()
        self.user_ffsake_enable.set()

    def run(self):
        try:
            while True:
                if gremlin.event_handler.EventListener().gremlin_active:
                    if fffsake.IsFffsakeActive():
                        if not self.user_ffsake_enable.is_set():
                            ShutDown()
                    elif self.user_ffsake_enable.is_set():
                        StartUp()
                elif fffsake.IsFffsakeActive():
                    ShutDown()
                time.sleep(1)
                # Better than self.daemon since we can ShutDown before exiting.
                if not threading.main_thread().is_alive():
                    ShutDown()
                    break
        except Exception as e:
            gremlin.util.log("FFFSake thread exception %r" % e)


class PluginState:
    def __init__(self):
        self.activator = ActivationThread()
        self.activator.start()

    def user_toggle(self):
        if self.activator.user_ffsake_enable.is_set():
            gremlin.util.log("FFFSake disable requested")
            self.activator.user_ffsake_enable.clear()
        else:
            gremlin.util.log("FFFSake enable requested")
            self.activator.user_ffsake_enable.set()


def _plugin_state():
    carrier = gremlin.event_handler.EventListener()
    if not hasattr(carrier, "_fffsake_state"):
        carrier._fffsake_state = PluginState()
    return carrier._fffsake_state


_state = _plugin_state()


@decorator_ffb_toggle.button(ffb_toggle.input_id)
def ffb_toggle_handler(event):
    # Button press generates two events; act only on one of them.
    if event.is_pressed:
        _state.user_toggle()
