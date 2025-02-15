[//]: # "© 2025 Code Monet <code.monet@proton.me>"

## Joystick as Handbrake

If you want to use an analog axis (usually throttle on a HOTAS, or the Y axis of
the joystick) as a handbrake in your driving game,
typically you should just be able to bind it. Some games however expect
a "toggle" rather than "held" control. You may also want to configure the
"bite" point. This plugin will let you achieve that.

### Setup

In your desired Joystick Gremlin profile, go to the `Plugins` tab and add
the Handbrake plugin (`joystick_gremlin/plugins/handbrake.py`). The following
configuration is needed:

*   `Handbrake Output (vjoy)` - vJoy button to use for handbrake output.
*   `Handbrake input axis` - Physical axis to use for handbrake.

TODO: Add option for bite point.

### Usage

The best way to understand this plugin is to enable it, open "Input Viewer"
in Joystick Gremlin, and play with the handbrake control.

### Known Compatible Games

This plugin is more useful for games that have toggle handbrake.

*   American Truck Simulator (toggle)
*   Euro Truck Simulator 2 (toggle)
