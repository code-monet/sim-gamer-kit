"""Joystick Gremlin plugin to use a joystick (throttle) as a handbrake."""

import time

import gremlin
from gremlin.user_plugin import *
from gremlin import util

mode = ModeVariable("Mode", "The mode to use for this mapping")

# vJoy outputs.

# Handbrakes may or may not be "hold" per the game.
handbrake_output_button = VirtualInputVariable(
    "Handbrake Output (vjoy)",
    "vJoy button to use for handbrake output",
    [gremlin.common.InputType.JoystickButton],
)

# TODO: Use boolean variable to change behavior.
handbrake_is_toggle = BoolVariable(
    "Handbrake output is toggle (vs hold)",
    (
        "Set True if the handbrake control in game is toggle, "
        "False if the game expects it to be held"
    ),
    True,
)

# Physical inputs - the joystick axis (usually throttle or slider without a spring).
handbrake_input_axis = PhysicalInputVariable(
    "Handbrake input axis (throttle or slider)",
    "Axis to use for handbrake input.",
    [gremlin.common.InputType.JoystickAxis],
)

decorator_h = handbrake_input_axis.create_decorator(mode.value)


# Plugin-specific data and functions.
class PluginState:
    """Stores all the state needed by this plugin."""

    parking_state: bool = False
    parking_axis: float = 0
    parking_change_time: float = 0


plugin_state = PluginState()


def update_handbrake(vjoy):
    global plugin_state
    device = vjoy[handbrake_output_button.value["device_id"]]
    # Generate an event when the axis is pushed away or returned to center.
    # TODO Set these values via input variables.
    if (plugin_state.parking_axis < -0.8 and not plugin_state.parking_state) or (
        -0.2 < plugin_state.parking_axis < 0.2 and plugin_state.parking_state
    ):
        device.button(handbrake_output_button.value["input_id"]).is_pressed = True
        plugin_state.parking_change_time = time.monotonic()
        plugin_state.parking_state = not plugin_state.parking_state
    if (
        plugin_state.parking_change_time
        and time.monotonic() - plugin_state.parking_change_time > 0.15
    ):
        device.button(handbrake_output_button.value["input_id"]).is_pressed = False
        plugin_state.parking_change_time = 0
    # util.log(f"Parking state {plugin_state.parking_state}")


# Physical input handlers.
@decorator_h.axis(handbrake_input_axis.input_id)
def axis_handbrake_handler(event, vjoy):
    global plugin_state
    plugin_state.parking_axis = event.value
    update_handbrake(vjoy)


# Resetter that we don't rely on because of bug with periodic handlers.
@gremlin.input_devices.periodic(0.25)
def handbrake_periodic_update(vjoy):
    update_handbrake(vjoy)
