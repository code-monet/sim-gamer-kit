"""Joystick Gremlin plugin to use a joystick as an H-shifter."""

import enum

import gremlin
from gremlin.user_plugin import *
from gremlin import util

mode = ModeVariable("Mode", "The mode to use for this mapping")

# vJoy outputs. We probably need a different script for games that allow keyboard
# to be used for gear selection.

# H-shifters work by holding the button down for whichever gear is active.
gear_1 = VirtualInputVariable(
    "Gear 1", "vJoy button to use for gear 1", [gremlin.common.InputType.JoystickButton]
)
gear_2 = VirtualInputVariable(
    "Gear 2", "vJoy button to use for gear 2", [gremlin.common.InputType.JoystickButton]
)
gear_3 = VirtualInputVariable(
    "Gear 3", "vJoy button to use for gear 3", [gremlin.common.InputType.JoystickButton]
)
gear_4 = VirtualInputVariable(
    "Gear 4", "vJoy button to use for gear 4", [gremlin.common.InputType.JoystickButton]
)
gear_5 = VirtualInputVariable(
    "Gear 5", "vJoy button to use for gear 5", [gremlin.common.InputType.JoystickButton]
)
gear_6 = VirtualInputVariable(
    "Gear 6", "vJoy button to use for gear 6", [gremlin.common.InputType.JoystickButton]
)
gear_r = VirtualInputVariable(
    "Reverse (output)",
    "vJoy button to use for reverse gear",
    [gremlin.common.InputType.JoystickButton],
)

# TODO: Use boolean variable to change behavior for non-centering axes.
axes_are_self_centering = BoolVariable(
    "Axes are self-centering",
    (
        "Set True if the axes are self-centering with a spring, "
        "False if they don't return to neutral without user input"
    ),
    False,
)

# Physical inputs - the joystick axes and a button to go to neutral.
btn_neutral = PhysicalInputVariable(
    "Neutral",
    "Button to set gear to neutral. Needed for self-centering axes.",
    [gremlin.common.InputType.JoystickButton],
)
btn_reverse = PhysicalInputVariable(
    "Reverse (input)",
    "Button to set gear to reverse. Needed because we have 6 positions only via the axes.",
    [gremlin.common.InputType.JoystickButton],
)
axis_x = PhysicalInputVariable(
    "Left-right axis",
    "Left-right axis to use for H-shifter.",
    [gremlin.common.InputType.JoystickAxis],
)
axis_y = PhysicalInputVariable(
    "Up-down axis",
    "Up-down axis to use for H-shifter.",
    [gremlin.common.InputType.JoystickAxis],
)

decorator_n = btn_neutral.create_decorator(mode.value)
decorator_r = btn_reverse.create_decorator(mode.value)
decorator_x = axis_x.create_decorator(mode.value)
decorator_y = axis_y.create_decorator(mode.value)


# Plugin-specific data and functions.
class Gear(enum.Enum):
    GEAR_1 = enum.auto()
    GEAR_2 = enum.auto()
    GEAR_3 = enum.auto()
    GEAR_4 = enum.auto()
    GEAR_5 = enum.auto()
    GEAR_6 = enum.auto()
    GEAR_N = enum.auto()
    GEAR_R = enum.auto()


GEAR_BUTTONS = {
    Gear.GEAR_1: gear_1,
    Gear.GEAR_2: gear_2,
    Gear.GEAR_3: gear_3,
    Gear.GEAR_4: gear_4,
    Gear.GEAR_5: gear_5,
    Gear.GEAR_6: gear_6,
    Gear.GEAR_R: gear_r,
}


class PluginState:
    """Stores all the state needed by this plugin."""

    current_gear: Gear = Gear.GEAR_N
    x_pos: float = 0
    y_pos: float = 0
    neutral_pressed: bool = False
    reverse_pressed: bool = False


plugin_state = PluginState()


def update_gear(vjoy):
    global plugin_state
    if plugin_state.neutral_pressed:
        plugin_state.current_gear = Gear.GEAR_N
    elif plugin_state.reverse_pressed:
        plugin_state.current_gear = Gear.GEAR_R
    else:
        x_axis = plugin_state.x_pos
        y_axis = plugin_state.y_pos
        if x_axis < -0.9 and y_axis < -0.9:
            plugin_state.current_gear = Gear.GEAR_1
        elif x_axis < -0.9 and y_axis > 0.9:
            plugin_state.current_gear = Gear.GEAR_2
        elif -0.25 < x_axis < 0.25 and y_axis < -0.9:
            plugin_state.current_gear = Gear.GEAR_3
        elif -0.25 < x_axis < 0.25 and y_axis > 0.9:
            plugin_state.current_gear = Gear.GEAR_4
        elif x_axis > 0.9 and y_axis < -0.9:
            plugin_state.current_gear = Gear.GEAR_5
        elif x_axis > 0.9 and y_axis > 0.9:
            plugin_state.current_gear = Gear.GEAR_6
    util.log(f"Gear {plugin_state.current_gear}")
    for gear, gear_button in GEAR_BUTTONS.items():
        device = vjoy[gear_button.value["device_id"]]
        device.button(gear_button.value["input_id"]).is_pressed = (
            gear == plugin_state.current_gear
        )


def set_state(vjoy):
    device = vjoy[gear_1.value["device_id"]]
    device.button(gear_1.value["input_id"]).is_prssed = False


# Physical input handlers.
@decorator_x.axis(axis_x.input_id)
def axis_x_handler(event, vjoy):
    global plugin_state
    plugin_state.x_pos = event.value
    update_gear(vjoy)


@decorator_y.axis(axis_y.input_id)
def axis_y_handler(event, vjoy):
    global plugin_state
    plugin_state.y_pos = event.value
    update_gear(vjoy)


@decorator_n.button(btn_neutral.input_id)
def btn_neutral_handler(event, vjoy):
    global plugin_state
    plugin_state.neutral_pressed = event.is_pressed
    update_gear(vjoy)


@decorator_r.button(btn_reverse.input_id)
def btn_reverse_handler(event, vjoy):
    global plugin_state
    plugin_state.reverse_pressed = event.is_pressed
    update_gear(vjoy)
