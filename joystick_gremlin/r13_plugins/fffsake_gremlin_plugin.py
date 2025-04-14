"""© 2025 Code Monet <code.monet@proton.me>

Joystick Gremlin plugin for FFFSake.
"""

import inspect
import os.path
import sys
import threading
import time

import gremlin.common
import gremlin.event_handler
import gremlin.joystick_handling
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

# Fix for the situation where issued effects are lost if Gremlin hasn't
# acquired the vJoy device yet. (Value is used later, listed here as an option of sorts).
# This logic could be smarter.
VJOY_DEVICES_TO_ACQUIRE = [1]


mode = ModeVariable("Mode", "The mode to use for this mapping")
ffb_toggle = PhysicalInputVariable(
    "Mute/Unmute Force Feedback",
    "Button to mute/unmute Force Feedback. Can be on any device",
    [gremlin.common.InputType.JoystickButton],
)
decorator_ffb_toggle = ffb_toggle.create_decorator(mode.value)


###############################################################################
class PluginOptions:
    """All FFFSake Plug-in Options."""


PLUGIN_OPTIONS = PluginOptions()

# For some reason, saving these directly to PLUGIN_OPTIONS causes them to not register.
option_constant_gain = IntegerVariable(
    "Constant Gain %",
    "User gain setting for all constant effects",
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_ramp_gain = IntegerVariable(
    "Ramp Gain %",
    "User gain setting for all ramp effects",
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_sine_gain = IntegerVariable(
    "Sine Gain %",
    "User gain setting for all sine effects",
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_square_gain = IntegerVariable(
    "Square Gain %",
    "User gain setting for all square effects",
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_triangle_gain = IntegerVariable(
    "Triangle Gain %",
    "User gain setting for all triangle effects",
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_sawtooth_up_gain = IntegerVariable(
    "Sawtooth Up Gain %",
    "User gain setting for all sawtooth up effects",
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_sawtooth_down_gain = IntegerVariable(
    "Sawtooth Down Gain %",
    "User gain setting for all sawtooth down effects",
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_spring_gain = IntegerVariable(
    "Spring Gain %",
    "User gain setting for all spring effects",
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_damper_gain = IntegerVariable(
    "Damper Gain %",
    "User gain setting for all damper effects",
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_inertia_gain = IntegerVariable(
    "Inertia Gain %",
    "User gain setting for all inertia effects",
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_friction_gain = IntegerVariable(
    "Friction Gain %",
    "User gain setting for all friction effects",
    initial_value=100,
    min_value=0,
    max_value=300,
)


def _process_registry_value(self, value):
    return str(value)


SelectionVariable._process_registry_value = _process_registry_value

_FORWARDER = "Forwarder"
_REDUCER = "Reducer"
option_engine_selector = SelectionVariable(
    "FFFSake Engine",
    "Which FFFSake engine to use. Wheels can use either, joysticks should use Forwarder",
    [_FORWARDER, _REDUCER],
    is_optional=True,
)
# Doesn't work if the user has multiple devices with the
# same name - this is unlikely to need support.
# TODO: This list only populates at Gremlin launch, and after each "Activate".
try:
    option_device_selector = SelectionVariable(
        "FF Device",
        "Which device to send force feedback commands to.",
        [d.name for d in fffsake.DetectFfbDevices() if not d.is_virtual],
        is_optional=True,
    )
except AssertionError:
    # Our best guess as to why this might happen:
    gremlin.util.display_error(
        "FFFSake plugins says: No FFB-capable devices;"
        " please connect/power on your FFB device and restart Gremlin."
    )

PLUGIN_OPTIONS.constant_gain = option_constant_gain
PLUGIN_OPTIONS.ramp_gain = option_ramp_gain
PLUGIN_OPTIONS.sine_gain = option_sine_gain
PLUGIN_OPTIONS.square_gain = option_square_gain
PLUGIN_OPTIONS.triangle_gain = option_triangle_gain
PLUGIN_OPTIONS.sawtooth_up_gain = option_sawtooth_up_gain
PLUGIN_OPTIONS.sawtooth_down_gain = option_sawtooth_down_gain
PLUGIN_OPTIONS.spring_gain = option_spring_gain
PLUGIN_OPTIONS.damper_gain = option_damper_gain
PLUGIN_OPTIONS.inertia_gain = option_inertia_gain
PLUGIN_OPTIONS.friction_gain = option_friction_gain
PLUGIN_OPTIONS.engine_selector = option_engine_selector
PLUGIN_OPTIONS.device_selector = option_device_selector


def MakeFffsakeOptions(plugin_options):
    opt = fffsake.FffsakeOptions()
    opt.engine_options.set_device_gain(1)
    opt.engine_options.set_constant_gain(plugin_options.constant_gain.value / 100)
    opt.engine_options.set_ramp_gain(plugin_options.ramp_gain.value / 100)
    opt.engine_options.set_sine_gain(plugin_options.sine_gain.value / 100)
    opt.engine_options.set_square_gain(plugin_options.square_gain.value / 100)
    opt.engine_options.set_triangle_gain(plugin_options.triangle_gain.value / 100)
    opt.engine_options.set_sawtooth_up_gain(plugin_options.sawtooth_up_gain.value / 100)
    opt.engine_options.set_sawtooth_down_gain(
        plugin_options.sawtooth_down_gain.value / 100
    )
    opt.engine_options.set_spring_gain(plugin_options.spring_gain.value / 100)
    opt.engine_options.set_damper_gain(plugin_options.damper_gain.value / 100)
    opt.engine_options.set_inertia_gain(plugin_options.inertia_gain.value / 100)
    opt.engine_options.set_friction_gain(plugin_options.friction_gain.value / 100)
    return opt


###############################################################################
# Plugin functionality.


def StartUp(plugin_options):
    """Start up the FFFSake plugin.

    This function may not be thread-safe and should only be called inside the activation thread.
    """
    gremlin.util.log("FFB Device selected: %s" % plugin_options.device_selector.value)
    guid = None
    for d in fffsake.DetectFfbDevices():
        if not d.is_virtual and d.name == plugin_options.device_selector.value:
            guid = d.guid
            break
    else:
        gremlin.util.display_error(
            "Device (no longer?) present: %s" % plugin_options.device_selector.value
        )
        return
    if plugin_options.engine_selector.value == _FORWARDER:
        fffsake.RegisterFffsakeForwarder(guid)
    elif plugin_options.engine_selector.value == _REDUCER:
        fffsake.RegisterFffsakeReducer(guid)
    else:
        gremlin.util.log(
            "FFFSake plugin: Unknown engine selected: %s"
            % plugin_options.engine_selector.value
        )
    gremlin.util.log(f"FFFSake {plugin_options.engine_selector.value} engine active")


def ShutDown():
    fffsake.FffsakeCleanup()
    gremlin.util.log("FFFSake disabled")


class ActivationThread(threading.Thread):
    """Thread that activates/deactivates fffsake with Gremlin activation.

    Threading was chosen to implement the functionality of detecting that Joystick
    Gremlin is "active" and to tie FFFSake registration lifetime to that.
    Thread exits when the main thread exits.
    """

    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        # Only use properties to access.
        # Thread changes this to None once it has been "consumed". Thread
        # will retry until FFFSake is active.
        self._fffsake_options = None
        # The corresponding property must be set for FFFSake to activate.
        self._plugin_options = None

    def run(self):
        try:
            while True:
                if gremlin.event_handler.EventListener().gremlin_active:
                    plugin_options = self.plugin_options  # Lock, retrieve.
                    if not fffsake.IsFffsakeActive() and plugin_options is not None:
                        # Fix for effects being missed if they are issued before Gremlin
                        # actually decides to acquire the vJoy device.
                        for vjoy_device in VJOY_DEVICES_TO_ACQUIRE:
                            # Acquires the device.
                            gremlin.joystick_handling.VJoyProxy()[vjoy_device]
                        StartUp(plugin_options)
                    if fffsake.IsFffsakeActive():
                        fffsake_options = self.fffsake_options  # Lock, retrieve.
                        if fffsake_options is not None:
                            fffsake.SetFffsakeOptions(fffsake_options)
                            del self.fffsake_options
                elif fffsake.IsFffsakeActive():
                    ShutDown()
                # Better than self.daemon since we can ShutDown() before exiting.
                if not threading.main_thread().is_alive():
                    ShutDown()
                    break
                time.sleep(1)
        except Exception as e:
            gremlin.util.log("FFFSake thread exception %r" % e)

    @property
    def fffsake_options(self):
        with self._lock:
            return self._fffsake_options

    @fffsake_options.setter
    def fffsake_options(self, value):
        with self._lock:
            self._fffsake_options = value

    @fffsake_options.deleter
    def fffsake_options(self):
        with self._lock:
            self._fffsake_options = None

    @property
    def plugin_options(self):
        with self._lock:
            return self._plugin_options

    @plugin_options.setter
    def plugin_options(self, value):
        with self._lock:
            self._plugin_options = value


class PluginState:
    """Class used to maintain plugin state across potentially multiple imports of the plugin."""

    def __init__(self):
        self.activator = ActivationThread()
        # This has the effect of starting the thread on first plugin import. The thread
        # will exit when Joystick Gremlin exits.
        self.activator.start()
        self._user_mute = False

    def user_toggle(self):
        if self._user_mute:
            gremlin.util.log("Force feedback unmute requested")
            self._user_mute = False
            # Don't MakeOptions() here; the values are taken from some
            # stale scope. Options have been set earlier in the call
            # stack from the "live" scope.
        else:
            gremlin.util.log("Force Feedback mute requested")
            self._user_mute = True
            self.activator.fffsake_options.engine_options.set_device_gain(0)


def _plugin_state(plugin_options):
    carrier = gremlin.event_handler.EventListener()  # Singleton.
    if not hasattr(carrier, "_fffsake_state"):
        carrier._fffsake_state = PluginState()
    return carrier._fffsake_state


_state = _plugin_state(PLUGIN_OPTIONS)
_state.activator.fffsake_options = MakeFffsakeOptions(PLUGIN_OPTIONS)
_state.activator.plugin_options = PLUGIN_OPTIONS


@decorator_ffb_toggle.button(ffb_toggle.input_id)
def ffb_toggle_handler(event):
    # Button press generates two events; act only on one of them.
    if event.is_pressed:
        # Overwritten if muting, used if unmuting.
        # This needs to be set here; there's some funny scope/environment business
        # going on.
        _state.activator.fffsake_options = MakeFffsakeOptions(PLUGIN_OPTIONS)
        _state.user_toggle()
