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
    "Mute/Unmute Force Feedback",
    "Button to mute/unmute Force Feedback. Can be on any device",
    [gremlin.common.InputType.JoystickButton],
)
decorator_ffb_toggle = ffb_toggle.create_decorator(mode.value)

###############################################################################
# All FFFSake options.
option_constant_gain = IntegerVariable(
    "Constant Gain %",
    "User gain setting for all constant effects",
    initial_value=50,
    min_value=0,
    max_value=100,
)
option_ramp_gain = IntegerVariable(
    "Ramp Gain %",
    "User gain setting for all ramp effects",
    initial_value=50,
    min_value=0,
    max_value=100,
)
option_sine_gain = IntegerVariable(
    "Sine Gain %",
    "User gain setting for all sine effects",
    initial_value=50,
    min_value=0,
    max_value=100,
)
option_square_gain = IntegerVariable(
    "Square Gain %",
    "User gain setting for all square effects",
    initial_value=50,
    min_value=0,
    max_value=100,
)
option_triangle_gain = IntegerVariable(
    "Triangle Gain %",
    "User gain setting for all triangle effects",
    initial_value=50,
    min_value=0,
    max_value=100,
)
option_sawtooth_up_gain = IntegerVariable(
    "Sawtooth Up Gain %",
    "User gain setting for all sawtooth up effects",
    initial_value=50,
    min_value=0,
    max_value=100,
)
option_sawtooth_down_gain = IntegerVariable(
    "Sawtooth Down Gain %",
    "User gain setting for all sawtooth down effects",
    initial_value=50,
    min_value=0,
    max_value=100,
)
option_spring_gain = IntegerVariable(
    "Spring Gain %",
    "User gain setting for all spring effects",
    initial_value=50,
    min_value=0,
    max_value=100,
)
option_damper_gain = IntegerVariable(
    "Damper Gain %",
    "User gain setting for all damper effects",
    initial_value=50,
    min_value=0,
    max_value=100,
)
option_inertia_gain = IntegerVariable(
    "Inertia Gain %",
    "User gain setting for all inertia effects",
    initial_value=50,
    min_value=0,
    max_value=100,
)
option_friction_gain = IntegerVariable(
    "Friction Gain %",
    "User gain setting for all friction effects",
    initial_value=50,
    min_value=0,
    max_value=100,
)


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


def MakeOptions():
    opt = fffsake.FffsakeOptions()
    opt.engine_options.set_constant_gain(option_constant_gain.value / 100)
    opt.engine_options.set_ramp_gain(option_ramp_gain.value / 100)
    opt.engine_options.set_sine_gain(option_sine_gain.value / 100)
    opt.engine_options.set_square_gain(option_square_gain.value / 100)
    opt.engine_options.set_triangle_gain(option_triangle_gain.value / 100)
    opt.engine_options.set_sawtooth_up_gain(option_sawtooth_up_gain.value / 100)
    opt.engine_options.set_sawtooth_down_gain(option_sawtooth_down_gain.value / 100)
    opt.engine_options.set_spring_gain(option_spring_gain.value / 100)
    opt.engine_options.set_damper_gain(option_damper_gain.value / 100)
    opt.engine_options.set_inertia_gain(option_inertia_gain.value / 100)
    opt.engine_options.set_friction_gain(option_friction_gain.value / 100)
    return opt


def MakeMutingOptions():
    opt = MakeOptions()
    opt.engine_options.set_constant_gain(0)
    opt.engine_options.set_ramp_gain(0)
    opt.engine_options.set_sine_gain(0)
    opt.engine_options.set_square_gain(0)
    opt.engine_options.set_triangle_gain(0)
    opt.engine_options.set_sawtooth_up_gain(0)
    opt.engine_options.set_sawtooth_down_gain(0)
    opt.engine_options.set_spring_gain(0)
    opt.engine_options.set_damper_gain(0)
    opt.engine_options.set_inertia_gain(0)
    opt.engine_options.set_friction_gain(0)
    return opt

###############################################################################
# Plugin functionality.

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
        self._lock = threading.Lock()
        # Only use properties to access.
        # Thread changes this to None once it has been "consumed". Thread
        # will retry until FFFSake is active.
        self._options = MakeOptions()

    def run(self):
        try:
            while True:
                if gremlin.event_handler.EventListener().gremlin_active:
                    if not fffsake.IsFffsakeActive():
                        StartUp()
                    
                    if fffsake.IsFffsakeActive():
                        options = self.options  # Lock once and retrieve value.
                        if options is not None:
                            fffsake.SetFffsakeOptions(options)
                            del self.options
                elif fffsake.IsFffsakeActive():
                    ShutDown()
                time.sleep(1)
                # Better than self.daemon since we can ShutDown before exiting.
                if not threading.main_thread().is_alive():
                    ShutDown()
                    break
        except Exception as e:
            gremlin.util.log("FFFSake thread exception %r" % e)
    
    @property
    def options(self):
        with self._lock:
            return self._options

    @options.setter
    def options(self, value):
        with self._lock:
            self._options = value
    
    @options.deleter
    def options(self):
        with self._lock:
            self._options = None


class PluginState:
    def __init__(self):
        self.activator = ActivationThread()
        self.activator.start()
        self._user_mute = False

    def user_toggle(self):
        if self._user_mute:
            gremlin.util.log("Force feedback unmute requested")
            self._user_mute = False
            # Don't MakeOptions() here; the values are taken from some
            # stale scope. Options have been set higher up in the call
            # stack from the "live" scope.
        else:
            gremlin.util.log("Force Feedback mute requested")
            self._user_mute = True
            self.activator.options = MakeMutingOptions()


def _plugin_state():
    carrier = gremlin.event_handler.EventListener()
    if not hasattr(carrier, "_fffsake_state"):
        carrier._fffsake_state = PluginState()
    return carrier._fffsake_state


_state = _plugin_state()
_state.activator.options = MakeOptions()


@decorator_ffb_toggle.button(ffb_toggle.input_id)
def ffb_toggle_handler(event):
    # Button press generates two events; act only on one of them.
    if event.is_pressed:
        # Overwritten if muting, used if unmuting.
        # This needs to be set here; there's some funny scoping business
        # going on.
        _state.activator.options = MakeOptions()
        _state.user_toggle()
