"""© 2025 Code Monet <code.monet@proton.me>

Joystick Gremlin plugin to use a joystick as an H-shifter.
"""

import enum

from gremlin import common
from gremlin import user_script
from gremlin import util

# Values may not be suitable for all joysticks especially on the corners.
AXIS_ENTRY_THRESHOLD = 0.9
AXIS_EXIT_THRESHOLD = 0.7  # Must be less than the above.
AXIS_NEUTRAL_ZONE = 0.25  # Must be less than the above.

mode = user_script.ModeVariable(
    "Mode", "The mode to use for this mapping", is_optional=True
)

# vJoy outputs. We probably need a different script for games that allow keyboard
# to be used for gear selection.

# H-shifters work by holding the button down for whichever gear is active.
gear_1 = user_script.VirtualInputVariable(
    "Gear 1",
    "vJoy button to use for gear 1",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)
gear_2 = user_script.VirtualInputVariable(
    "Gear 2",
    "vJoy button to use for gear 2",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)
gear_3 = user_script.VirtualInputVariable(
    "Gear 3",
    "vJoy button to use for gear 3",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)
gear_4 = user_script.VirtualInputVariable(
    "Gear 4",
    "vJoy button to use for gear 4",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)
gear_5 = user_script.VirtualInputVariable(
    "Gear 5",
    "vJoy button to use for gear 5",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)
gear_6 = user_script.VirtualInputVariable(
    "Gear 6",
    "vJoy button to use for gear 6",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)
gear_7 = user_script.VirtualInputVariable(
    "Gear 7",
    "vJoy button to use for gear 7",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)
gear_r = user_script.VirtualInputVariable(
    "Reverse (output)",
    "vJoy button to use for reverse gear",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)

# TODO: Use boolean variable to change behavior for non-centering axes.
# axes_are_self_centering = user_script.BoolVariable(
#     "Axes are self-centering",
#     (
#         "Set True if the axes are self-centering with a spring, "
#         "False if they don't return to neutral without user input"
#     ),
#     is_optional=True,
#     initial_value=True,
# )

# Physical inputs - the joystick axes (6 gears) and buttons to go to neutral and reverse.
btn_neutral = user_script.PhysicalInputVariable(
    "Neutral",
    "Button to set gear to neutral. Needed for self-centering axes.",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)
btn_reverse = user_script.PhysicalInputVariable(
    "Reverse (input)",
    "Button to set gear to reverse. Needed because we have 6 positions only via the axes.",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)
btn_7th = user_script.PhysicalInputVariable(
    "Gear 7 (input)",
    "Button to set gear 7. Needed because we have 6 positions only via the axes.",
    is_optional=False,
    valid_types=[common.InputType.JoystickButton],
)
axis_x = user_script.PhysicalInputVariable(
    "Left-right axis",
    "Left-right axis to use for H-shifter.",
    is_optional=False,
    valid_types=[common.InputType.JoystickAxis],
)
axis_y = user_script.PhysicalInputVariable(
    "Up-down axis",
    "Up-down axis to use for H-shifter.",
    is_optional=False,
    valid_types=[common.InputType.JoystickAxis],
)


# Plugin-specific data and functions.
class Gear(enum.Enum):
    GEAR_1 = enum.auto()
    GEAR_2 = enum.auto()
    GEAR_3 = enum.auto()
    GEAR_4 = enum.auto()
    GEAR_5 = enum.auto()
    GEAR_6 = enum.auto()
    GEAR_7 = enum.auto()
    GEAR_N = enum.auto()
    GEAR_R = enum.auto()


GEAR_BUTTONS = {
    Gear.GEAR_1: gear_1,
    Gear.GEAR_2: gear_2,
    Gear.GEAR_3: gear_3,
    Gear.GEAR_4: gear_4,
    Gear.GEAR_5: gear_5,
    Gear.GEAR_6: gear_6,
    Gear.GEAR_7: gear_7,
    Gear.GEAR_R: gear_r,
}


class PluginState:
    """Stores all the state needed by this plugin."""

    current_gear: Gear = Gear.GEAR_N
    x_pos: float = 0
    y_pos: float = 0
    neutral_pressed: bool = False
    reverse_pressed: bool = False
    gear7_pressed: bool = False


plugin_state = PluginState()


def update_gear():
    global plugin_state
    if plugin_state.neutral_pressed:
        plugin_state.current_gear = Gear.GEAR_N
    elif plugin_state.reverse_pressed:
        plugin_state.current_gear = Gear.GEAR_R
    elif plugin_state.gear7_pressed:
        plugin_state.current_gear = Gear.GEAR_7
    else:
        x_axis = plugin_state.x_pos
        y_axis = plugin_state.y_pos
        # We want to indicate "neutral" if we are about to change gears.
        approaching_gear = None
        # current_gear is only updated when in a gear zone.
        # This way it doesn't reset to neutral on its own.

        if x_axis < -AXIS_ENTRY_THRESHOLD:
            if y_axis < -AXIS_ENTRY_THRESHOLD:
                plugin_state.current_gear = Gear.GEAR_1
            elif y_axis < -AXIS_EXIT_THRESHOLD:
                approaching_gear = Gear.GEAR_1
            elif y_axis > AXIS_ENTRY_THRESHOLD:
                plugin_state.current_gear = Gear.GEAR_2
            elif y_axis > AXIS_EXIT_THRESHOLD:
                approaching_gear = Gear.GEAR_2
        elif -AXIS_NEUTRAL_ZONE < x_axis < AXIS_NEUTRAL_ZONE:
            if y_axis < -AXIS_ENTRY_THRESHOLD:
                plugin_state.current_gear = Gear.GEAR_3
            elif y_axis < -AXIS_EXIT_THRESHOLD:
                approaching_gear = Gear.GEAR_3
            elif y_axis > AXIS_ENTRY_THRESHOLD:
                plugin_state.current_gear = Gear.GEAR_4
            elif y_axis > AXIS_EXIT_THRESHOLD:
                approaching_gear = Gear.GEAR_4
        elif x_axis > AXIS_ENTRY_THRESHOLD:
            if y_axis < -AXIS_ENTRY_THRESHOLD:
                plugin_state.current_gear = Gear.GEAR_5
            elif y_axis < -AXIS_EXIT_THRESHOLD:
                approaching_gear = Gear.GEAR_5
            elif y_axis > AXIS_ENTRY_THRESHOLD:
                plugin_state.current_gear = Gear.GEAR_6
            elif y_axis > AXIS_EXIT_THRESHOLD:
                approaching_gear = Gear.GEAR_6
        # util.log(f"Gear {plugin_state.current_gear}")
        if (
            approaching_gear is not None
            and approaching_gear != plugin_state.current_gear
        ):
            plugin_state.current_gear = Gear.GEAR_N
    for gear, gear_button in GEAR_BUTTONS.items():
        gear_button.remap(gear == plugin_state.current_gear)


# Physical input handlers.
@axis_x.decorator(mode)
def axis_x_handler(event):
    global plugin_state
    plugin_state.x_pos = event.value
    update_gear()


@axis_y.decorator(mode)
def axis_y_handler(event):
    global plugin_state
    plugin_state.y_pos = event.value
    update_gear()


@btn_neutral.decorator(mode)
def btn_neutral_handler(event):
    global plugin_state
    plugin_state.neutral_pressed = event.is_pressed
    update_gear()


@btn_reverse.decorator(mode)
def btn_reverse_handler(event):
    global plugin_state
    plugin_state.reverse_pressed = event.is_pressed
    update_gear()


@btn_7th.decorator(mode)
def btn_7th_handler(event):
    global plugin_state
    plugin_state.gear7_pressed = event.is_pressed
    update_gear()
