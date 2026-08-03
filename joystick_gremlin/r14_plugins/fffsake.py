"""© 2025 Code Monet <code.monet@proton.me>

Joystick Gremlin R14+ plugin for FFFSake.
"""

import inspect
import os
import sys

from gremlin import error
from gremlin import signal
from gremlin import types
from gremlin import user_script
from gremlin import util
from gremlin.ui import backend

current_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
while True:
    head, tail = os.path.split(current_path)
    if tail == "joystick_gremlin":
        if head not in sys.path:
            # Insert instead of appending in case the user is using my
            # fork of Gremlin that already has FFFSake.
            sys.path.insert(0, head)
        break
    current_path = head

from fffsake.x64 import fffsake

from vjoy import vjoy


version_message = fffsake.GetVersionMismatchMessage()
if version_message:
    signal.display_error('FFFSake plugin vJoy version mismatch', version_message)

# Fix for the situation where issued effects are lost if Gremlin hasn't
# acquired the vJoy device yet. (Value is used later, listed here as an option of sorts).
# This logic could be smarter.
VJOY_DEVICES_TO_ACQUIRE = [1]

mode_var = user_script.ModeVariable(
    "Mode", "The mode to use for this plugin", is_optional=True
)
ffb_toggle = user_script.PhysicalInputVariable(
    "Mute/Unmute Force Feedback",
    "Button to mute/unmute Force Feedback. Can be on any device",
    is_optional=True,
    valid_types=[types.InputType.JoystickButton],
)


###############################################################################
class PluginOptions:
    """All FFFSake Plug-in Options."""


PLUGIN_OPTIONS = PluginOptions()

# Saving these directly to PLUGIN_OPTIONS causes them to not register.
# Because user_script.py:562 is "for key, value in self.module.__dict__.items():"

_FORWARDER = "Forwarder"
_REDUCER = "Reducer"
option_engine_selector = user_script.SelectionVariable(
    "FFFSake Engine",
    "Which FFFSake engine to use. Wheels can use either, joysticks should use Forwarder",
    is_optional=False,
    option_list=[_REDUCER, _FORWARDER],
    default_index=0,
)

# Device selection doesn't work if the user has multiple devices with the
# same name - this is unlikely to need support.


def _user_notified():
    """Use this to track whether the user has been notified already."""
    carrier = user_script
    if not hasattr(carrier, "_fffsake_user_notified"):
        carrier._fffsake_user_notified = True
        return False
    return carrier._fffsake_user_notified


detected_devices = [d.name for d in fffsake.DetectFfbDevices() if not d.is_virtual]
if not detected_devices and not _user_notified():
    signal.display_error(
        "FFFSake plugin inactive",
        "No FFB-capable devices; please connect/power on your FFB device."
    )
_FIRST_DEVICE_PLACEHOLDER = "First FFB Device"
option_device_selector = user_script.SelectionVariable(
    "FF Device",
    "Which device to send force feedback commands to.",
    is_optional=True,
    option_list=[_FIRST_DEVICE_PLACEHOLDER] + detected_devices,
    default_index=0,
)
_WHEEL = "Wheel"
_JOYSTICK = "Joystick"
option_device_type_selector = user_script.SelectionVariable(
    "FF Device Type",
    "(Reducer only) Whether the device is a FF wheel or joystick.",
    is_optional=True,
    option_list=[_WHEEL, _JOYSTICK],
    default_index=0,
)

option_device_gain = user_script.IntegerVariable(
    "Device Gain %",
    "User gain setting for all effects. May have no effect with forwarding engine.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=100,
)
option_constant_gain = user_script.IntegerVariable(
    "Constant Gain %",
    "User gain setting for all constant effects. Affects strength and limits.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_ramp_gain = user_script.IntegerVariable(
    "Ramp Gain %",
    "User gain setting for all ramp effects. Affects strength and limits.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_sine_gain = user_script.IntegerVariable(
    "Sine Gain %",
    "User gain setting for all sine effects. Affects strength and limits.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_square_gain = user_script.IntegerVariable(
    "Square Gain %",
    "User gain setting for all square effects. Affects strength and limits.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_triangle_gain = user_script.IntegerVariable(
    "Triangle Gain %",
    "User gain setting for all triangle effects. Affects strength and limits.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_sawtooth_up_gain = user_script.IntegerVariable(
    "Sawtooth Up Gain %",
    "User gain setting for all sawtooth up effects. Affects strength and limits.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_sawtooth_down_gain = user_script.IntegerVariable(
    "Sawtooth Down Gain %",
    "User gain setting for all sawtooth down effects. Affects strength and limits.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_spring_gain = user_script.IntegerVariable(
    "Spring Gain %",
    "User gain setting for all spring effects. Affects strength and limits.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_damper_gain = user_script.IntegerVariable(
    "Damper Gain %",
    "User gain setting for all damper effects. Affects strength and limits.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_inertia_gain = user_script.IntegerVariable(
    "Inertia Gain %",
    "User gain setting for all inertia effects. Affects strength and limits.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_friction_gain = user_script.IntegerVariable(
    "Friction Gain %",
    "User gain setting for all friction effects. Affects strength and limits.",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_spring_coefficient = user_script.IntegerVariable(
    "Spring Coefficient %",
    "User coefficient for all spring effects. Affects strength without changing limits",
    is_optional=True,
    initial_value=100,
    min_value=0,
    max_value=300,
)
option_friction_coefficient = user_script.IntegerVariable(
    "Friction Coefficient %",
    "Adjusts friction feeling; depends on device torque setting",
    is_optional=True,
    initial_value=50,
    min_value=0,
    max_value=1000,
)
option_compat_unminimize = user_script.BoolVariable(
    "Compatibility: Restore minimized forces",
    "Compatibility fix for games that unintentionally have zeroed forces that only work on some devices",
    is_optional=True,
    initial_value=False,
)
option_compat_force_restart = user_script.BoolVariable(
    "Compatibility: Force restart on update",
    "Compatibility fix for games that expect certain forces to be restarted when updated",
    is_optional=True,
    initial_value=False,
)
_Y_AXIS_HANDLING_AUTO = "Auto"
_Y_AXIS_HANDLING_ROTATE_TO_X = "Rotate to X"
option_y_axis_handling_selector = user_script.SelectionVariable(
    "Y-Axis Forces Handling",
    "(Debugging only) How to handle Y-axis forces",
    is_optional=True,
    option_list=[_Y_AXIS_HANDLING_AUTO, _Y_AXIS_HANDLING_ROTATE_TO_X],
    default_index=0,
)
option_device_update_period_ms = user_script.IntegerVariable(
    "Device Update Period (ms)",
    "Device update period in milliseconds. Allowed range: [1, 34].",
    is_optional=True,
    initial_value=5,
    min_value=1,
    max_value=34,
)

PLUGIN_OPTIONS.device_gain = option_device_gain
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
PLUGIN_OPTIONS.friction_coefficient = option_friction_coefficient
PLUGIN_OPTIONS.spring_coefficient = option_spring_coefficient
PLUGIN_OPTIONS.engine_selector = option_engine_selector
PLUGIN_OPTIONS.device_selector = option_device_selector
PLUGIN_OPTIONS.device_type_selector = option_device_type_selector
PLUGIN_OPTIONS.compat_unminimize = option_compat_unminimize
PLUGIN_OPTIONS.compat_force_restart = option_compat_force_restart
PLUGIN_OPTIONS.y_axis_handling_selector = option_y_axis_handling_selector
PLUGIN_OPTIONS.device_update_period_ms = option_device_update_period_ms


def MakeFffsakeOptions(plugin_options):
    opt = fffsake.FffsakeOptions()
    opt.device_options.set_device_gain(plugin_options.device_gain.value / 100)
    opt.device_options.set_constant_gain(plugin_options.constant_gain.value / 100)
    opt.device_options.set_ramp_gain(plugin_options.ramp_gain.value / 100)
    opt.device_options.set_sine_gain(plugin_options.sine_gain.value / 100)
    opt.device_options.set_square_gain(plugin_options.square_gain.value / 100)
    opt.device_options.set_triangle_gain(plugin_options.triangle_gain.value / 100)
    opt.device_options.set_sawtooth_up_gain(plugin_options.sawtooth_up_gain.value / 100)
    opt.device_options.set_sawtooth_down_gain(
        plugin_options.sawtooth_down_gain.value / 100
    )
    opt.device_options.set_spring_gain(plugin_options.spring_gain.value / 100)
    opt.device_options.set_damper_gain(plugin_options.damper_gain.value / 100)
    opt.device_options.set_inertia_gain(plugin_options.inertia_gain.value / 100)
    opt.device_options.set_friction_gain(plugin_options.friction_gain.value / 100)
    opt.device_options.set_spring_coefficient_multiplier(
        plugin_options.spring_coefficient.value / 100
    )
    opt.device_options.set_friction_coefficient_multiplier(
        plugin_options.friction_coefficient.value / 100
    )
    opt.device_options.set_compat_unminimize_forces(
        plugin_options.compat_unminimize.value
    )
    # Currently this option is only used for debugging. Users should probably leave this at True.
    opt.device_options.set_compat_unminimize_conditions(True)
    opt.device_options.set_compat_e_uprest(plugin_options.compat_force_restart.value)
    if plugin_options.y_axis_handling_selector.value == _Y_AXIS_HANDLING_ROTATE_TO_X:
        opt.y_forces_handling = fffsake.YForcesHandling.ROTATE_TO_X
    elif plugin_options.y_axis_handling_selector.value == _Y_AXIS_HANDLING_AUTO:
        opt.y_forces_handling = fffsake.YForcesHandling.AUTO
    else:
        util.log("Unknown Y-axis handling selector value")
        opt.y_forces_handling = fffsake.YForcesHandling.AUTO
    opt.set_device_update_period_ms(plugin_options.device_update_period_ms.value)
    return opt


###############################################################################
# Plugin functionality.


def StartUp(plugin_options: PluginOptions) -> bool:
    """Starts up the FFFSake plugin. Returns False if the device isn't found.

    This function may not be thread-safe and should only be called inside the activation thread.
    """
    util.log(
        f"FFFSake plugin attempting to start with device: {plugin_options.device_selector.value}"
    )
    if plugin_options.device_selector.value == _FIRST_DEVICE_PLACEHOLDER:
        use_first_device = True
        err_msg = (
            "FFFSake plugins says: No FFB-capable devices;"
            " please connect/power on your FFB device and reactivate Gremlin."
        )
    else:
        use_first_device = False
        err_msg = f"Device (no longer?) present:{plugin_options.device_selector.value}"
    guid = None
    activation_device = None
    for d in fffsake.DetectFfbDevices():
        if not d.is_virtual and (
            use_first_device or d.name == plugin_options.device_selector.value
        ):
            activation_device = d.name
            guid = d.guid
            break
    else:
        # util.display_error(err_msg)
        util.log(err_msg)
        return False
    util.log(
        f"FFB Device selected: {activation_device}, with {d.axes} axes, {d.buttons} buttons, {d.hats} hats. "
        f"FFB on X axis: {'Yes' if d.x_is_ffb else 'No'}, Y axis: {'Yes' if d.y_is_ffb else 'No'}"
    )

    # Fix for effects being missed if they are issued before Gremlin
    # actually decides to acquire the vJoy device.
    for vjoy_device in VJOY_DEVICES_TO_ACQUIRE:
        try:
            # Acquires the device.
            vjoy.VJoyProxy()[vjoy_device]
        except error.VJoyConcurrencyError as e:
            util.log(f"Couldn't re-acquire vJoy device {vjoy_device}, but should be okay to proceed: {e}")

    if plugin_options.engine_selector.value == _FORWARDER:
        fffsake.RegisterFffsakeForwarder(guid)
    elif plugin_options.engine_selector.value == _REDUCER:
        if plugin_options.device_type_selector.value == _WHEEL:
            fffsake.RegisterFffsakeReducer(guid, fffsake.UserReportedDeviceType.FFB_WHEEL)
        elif plugin_options.device_type_selector.value == _JOYSTICK:
            fffsake.RegisterFffsakeReducer(guid, fffsake.UserReportedDeviceType.FFB_JOYSTICK)
        else:
            util.log(
                f"FFFSake plugin: device type not known to plugin: {plugin_options.device_type_selector.value}"
            )
            return False
    else:
        util.log(
            f"FFFSake plugin: Unknown engine selected: {plugin_options.engine_selector.value}"
        )
        return False
    if fffsake.IsFffsakeActive():
        fffsake_options = MakeFffsakeOptions(plugin_options)
        fffsake.SetFffsakeOptions(fffsake_options)
        util.log(f"FFFSake {plugin_options.engine_selector.value} engine active")
        return True
    util.log("FFFSake could not be activated for unknown reasons")
    return False


def ShutDown():
    if fffsake.IsFffsakeActive():
        fffsake.FffsakeCleanup()
        util.log("FFFSake disabled")
    else:
        util.log("FFFSake was not active")


class PluginState:
    """Class used to maintain plugin state across potentially multiple imports of the plugin."""

    def __init__(self):
        self._user_mute = False
        self._is_running = False

    def should_mute(self) -> bool:
        """Toggles state and returns whether FFFSake should mute the device."""
        self._user_mute = not self._user_mute
        return self._user_mute
    
    def set_fffsake_running_state(self):
        if backend.Backend().runner.is_running():
            if not self._is_running:
                StartUp(PLUGIN_OPTIONS)
                self._is_running = True
        else:
            if self._is_running:
                ShutDown()
                self._is_running = False


def _plugin_state():
    carrier = user_script
    if not hasattr(carrier, "_fffsake_state"):
        carrier._fffsake_state = PluginState()
    return carrier._fffsake_state


backend.Backend().activityChanged.connect(_plugin_state().set_fffsake_running_state)


@ffb_toggle.decorator(mode_var)
def ffb_toggle_handler(event):
    # Button press generates two events; act only on one of them.
    if event.is_pressed and fffsake.IsFffsakeActive():
        fffsake_options = MakeFffsakeOptions(PLUGIN_OPTIONS)
        if _plugin_state().should_mute():
            util.log("Force feedback unmute requested")
            fffsake_options.device_options.set_device_gain(0)
        else:
            util.log("Force feedback mute requested")
        fffsake.SetFffsakeOptions(fffsake_options)
