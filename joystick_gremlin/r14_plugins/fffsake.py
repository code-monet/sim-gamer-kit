"""© 2025 Code Monet <code.monet@proton.me>

Joystick Gremlin R14 plugin for FFFSake.
"""

from gremlin import signal
from gremlin import types
from gremlin import user_script
from gremlin import util
from gremlin.ui import backend

from fffsake import fffsake

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

# TODO Change back to ints once they can be edited more easily.
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
PLUGIN_OPTIONS.spring_coefficient = option_spring_coefficient
PLUGIN_OPTIONS.engine_selector = option_engine_selector
PLUGIN_OPTIONS.device_selector = option_device_selector
PLUGIN_OPTIONS.compat_unminimize = option_compat_unminimize
PLUGIN_OPTIONS.compat_force_restart = option_compat_force_restart


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
    opt.engine_options.set_spring_coefficient_multiplier(
        plugin_options.spring_coefficient.value / 100
    )
    opt.engine_options.set_compat_unminimize_forces(
        plugin_options.compat_unminimize.value
    )
    opt.engine_options.set_compat_e_uprest(plugin_options.compat_force_restart.value)
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
    util.log(f"FFB Device selected: {activation_device}")

    # Fix for effects being missed if they are issued before Gremlin
    # actually decides to acquire the vJoy device.
    for vjoy_device in VJOY_DEVICES_TO_ACQUIRE:
        # Acquires the device.
        vjoy.VJoyProxy()[vjoy_device]

    if plugin_options.engine_selector.value == _FORWARDER:
        fffsake.RegisterFffsakeForwarder(guid)
    elif plugin_options.engine_selector.value == _REDUCER:
        fffsake.RegisterFffsakeReducer(guid)
    else:
        util.log(
            "FFFSake plugin: Unknown engine selected: %s"
            % plugin_options.engine_selector.value
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
            fffsake_options.engine_options.set_device_gain(0)
        else:
            util.log("Force feedback mute requested")
        fffsake.SetFffsakeOptions(fffsake_options)
