"""© 2025 Code Monet <code.monet@proton.me>

Joystick Gremlin plugin to use a joystick (throttle) as a handbrake.
"""

import time

from gremlin import common
from gremlin import user_script

mode_var = user_script.ModeVariable(
    "Mode", "The mode to use for this mapping", is_optional=True
)

# vJoy outputs.

# Handbrakes may or may not be "hold" per the game.
handbrake_output_button = user_script.VirtualInputVariable(
    "Handbrake Output (vjoy)",
    "vJoy button to use for handbrake output",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)

# TODO: Use boolean variable to change behavior.
handbrake_is_toggle = user_script.BoolVariable(
    "Handbrake output is toggle (vs hold)",
    (
        "Set True if the handbrake control in game is toggle, "
        "False if the game expects it to be held"
    ),
    is_optional=True,
    initial_value=True,
)

# Physical inputs - the joystick axis (usually throttle or slider without a spring).
handbrake_input_axis = user_script.PhysicalInputVariable(
    "Handbrake input axis (throttle or slider)",
    "Axis to use for handbrake input.",
    is_optional=False,
    valid_types=[common.InputType.JoystickAxis],
)


# Plugin-specific data and functions.
class PluginState:
    """Stores all the state needed by this plugin."""

    parking_state: bool = False
    parking_axis: float = 0
    parking_change_time: float = 0


plugin_state = PluginState()


def update_handbrake():
    global plugin_state
    # Generate an event when the axis is pushed away or returned to center.
    if (plugin_state.parking_axis < -0.8 and not plugin_state.parking_state) or (
        -0.2 < plugin_state.parking_axis < 0.2 and plugin_state.parking_state
    ):
        handbrake_output_button.remap(True)
        plugin_state.parking_change_time = time.monotonic()
        plugin_state.parking_state = not plugin_state.parking_state
    if (
        plugin_state.parking_change_time
        and time.monotonic() - plugin_state.parking_change_time > 0.15
    ):
        handbrake_output_button.remap(False)
        plugin_state.parking_change_time = 0
    # util.log(f"Parking state {plugin_state.parking_state}")


# Physical input handlers.
@handbrake_input_axis.decorator(mode_var)
def axis_handbrake_handler(event):
    global plugin_state
    plugin_state.parking_axis = event.value
    update_handbrake()


@user_script.periodic(0.15)
def handbrake_periodic_update():
    update_handbrake()
