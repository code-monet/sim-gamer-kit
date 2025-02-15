[//]: # "© 2025 Code Monet <code.monet@proton.me>"

# Sim Gamer Kit

A collection of tools for flight and driving simulation gamers on Windows.

## Installation

1.  Download the [latest release](https://github.com/code-monet/sim-gamer-kit/releases/latest)
2.  Extract the archive to a directory of your choice.
    1.  If you are upgrading versions, you can delete or overwrite the previous
        installation.

## Tools

### FFFSake, force feedback engine for vJoy

[FFFSake](./fffsake/index.md), or **F**or **F**orce **F**eedback's **Sake**, is:

*   Technically, a library that can bridge force feedback commands received by vJoy
    (virtual joystick) to a DirectInput compatible (physical) device.
*   Practically, a plugin to get force feedback effects on your wheel/joystick while your
    game is actually being played with vJoy, which is in turn being fed with inputs by
    an application like Joystick Gremlin.

### IndirectInput, compatibility fixes for DirectInput games and devices

[IndirectInput](./indirect_input/index.md) is a DLL-replacement based video game
compatibility fixer, focused on fixing issues seen when playing flight and racing games
with DirectInput devices.

## Joystick Gremlin Plugins

### Joystick as H-shifter

[Gremlin plugin](./joystick_gremlin_plugins/h_shifter.md) to use 2 analog axes
(typically a flight stick) as an H-shifter.

### Joystick as Handbrake

[Gremlin plugin](./joystick_gremlin_plugins/handbrake.md) to use an analog axis
(typically a flight throttle) as a handbrake.

## Game-Controller Compatibility Guides

A [collection of guides](./game_guides/index.md) for fixing input and force
feedback compatibility issues using tools in this kit.

## Hardware Compatibility Guides

A [collection of guides](./hardware_guides/index.md) describing common compatibility
issues with DirectInput devices.
