[//]: # "© 2025 Code Monet <code.monet@proton.me>"

# Driving and Flight Games Input/Force Feedback Guide

## How to use this guide

First, check the list of games below and see if it already has the game you're
looking for.

If not, you'll have to do some investigation yourself. First, check the list of
[controllers](../hardware_guides/index.md) and see if your device has known
compatibility issues.

Then check the list of [issues](./issues.md) to see if one or more matches what
you are seeing; try the suggested fixes. Please share your experience via
[GitHub Discussions](https://github.com/code-monet/sim-gamer-kit/discussions)
so I can grow this reference.

## Games With Known Compatibility Issues

Each game entry lists, in short form, the fixes that might be needed with some
or all DirectInput controllers.

The following short forms are used to refer to common [issues](./issues.md):

*   `Slip`: "FFB commands block game loop" fix is needed via FFFSake
*   `Combined pedals`: Two axes (usually accelerator and brake pedals) need to be
    combined into a single axis.
*   `Zeroed pedals`: An axis needs to be zeroed. Pedals and analog paddles on
    modern wheels are usually not zeroed.
*   `Hardware Effects Usage`: This can help explain why a game might not "feel
    right" on your force feedback device if the latter doesn't implement built-in
    effects properly. A rating is given out of:
    *   `High`: The game uses a lot of hardware FFB effects, and uses them in
        advanced ways.
    *   `Medium`: The game uses some hardware FFB effects in simple ways.
    *   `Minimal`: The game uses only constant and damper forces, the latter in
        very simple ways.
    *   `None`: The game only uses constant forces.
*   `FFB high effect count`: This game uses a large-ish number of FFB effects and
    is known to crash or lose effects with some wheels.
*   `FFB Saturation`: Force feedback from the game saturates; FFFSake user gain
    settings are advised.
*   `FFB Crash`: The game crashes if FFB devices are plugged in, or if FFB is enabled
    in-game.
*   `Requires Wheel`: The game requires the controller to identify as a wheel to enable
    certain features like axis curves, force feedback, or to configure the controller
    correctly.
*   `IndirectInput`: The game needs the listed feature from
    [IndirectInput](../indirect_input/index.md)

### Burnout Paradise

Also applies to the Remastered and Ultimate Box versions. This Criterion game has
a common issue with other Criterion racing games from this time that requires
forced wheel detection.

1.  Hardware Effects Usage: Medium
2.  Requires Wheel - without this, force feedback in game is disabled, or only applies
    to one side and many effects are missing.

### Bus Simulator 21

A driving game that curiously uses Unreal Engine, which may be to blame for compatibility
issues with FFB wheels:

1.  Requires Wheel - without this, there may be no force feedback in game.

> TODO: Game needs further study

### Crew 2

This game supports joystick, HOTAS and racing wheel input, the latter with force feedback.

1.  Slip: With force feedback wheels, FPS drops to less than 1.
2.  Hardware Effects Usage: Medium
3.  Requires Wheel. Without this, in-game wheel configuration is greyed out. Force
    feedback is half intensity and all axes default to "wild" curves (most noticeable
    as a massive dead zone in steering).

### Crew Motorfest

The wheel implementation has changed since `Crew 2` but has the same issues and then one more:

1.  FFB Crash: `HidHide` is needed to hide the problematic controller from the game, while
    using `vJoy` to play the game.
2.  Hardware Effects Usage: Medium
3.  Slip: FPS drop (like in previous versions of `Crew`) can be seen but is less extreme.

### Dirt 3

This game came out when H-shifters were rare. Even with the fix below, the shifter
will occasionally drop to neutral in-game; there is no known fix for that and appears
to be game logic.

1.  IndirectInput
    1.   Vendor spoof (only for H-shifters not made by a manufacturer in their
         hard-coded list). Without this, the in-game option to select
         manual transmission will be missing entirely.

### Dirt Rally

> TODO: Game available but study pending. The following are pending confirmation:

1.  IndirectInput
    1.   Vendor spoof (only for H-shifters not made by a manufacturer in their
         hard-coded list). Without this, the in-game option to select
         manual transmission will be missing entirely.
    2.   Full FFB configuration is not available with some wheels - fix unknown.
         TODO: Investigate creating a controller profile in the game directory as
         a fix.

### Dirt Rally 2.0

> TODO: Game available but study pending

### Elite: Dangerous

Only the first 32 buttons can be mapped from a single controller
([suspected source of limit](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee416627(v=vs.85))).
Players often use vJoy and Joystick Gremlin to map
buttons >= 32 from the physical device to the 0-31 range of buttons on vJoy.

This game does not have force feedback. It (probably still) does rumble on Xinput devices.

### GRID

> TODO: Game available but study pending

### Need for Speed: Most Wanted (2005)

An "arcade" racing game with one of the better force feedback effects for its time.
Known compatibility issues:

1.  Zeroed pedals
2.  Hardware Effects Usage: High
3.  FFB high effect count (partial loss of effects)
4.  FFB Saturation: Recommended **40%** for `Constant`, `Spring`, `Square` and `Sine`.
    Without this, road effects are lost when steering forces are strong.
5.  Don't bind handbrake to an analog axis, it can break auto-braking behavior for
    accelerator and reverse axes.

### Need for Speed: Heat

One of the few racing games I have seen that simply doesn't allow you to bind
controls! As of 2025, racing wheels are completely broken. I'm waiting for EA to
issue a fix, or otherwise I'll try implementing a fix in `IndirectInput`.

1.  Inability to bind controls. Use Joystick Gremlin and bind as follows:
    1.   TODO Fill this section
2.  Zeroed paddles (not pedals). TODO Confirm this.
3.  TODO: Fill out FFB information

### Need for Speed: Hot Pursuit (2010)

This Criterion game is similar to their other games from this time in terms of
DirectInput usage.

1.  Hardware Effects Usage: Medium
2.  Requires Wheel: Without this, an inferior, fallback
    model meant for joysticks is used; many effects are missing and forces are
    applied along the Y axis.
3.  Zeroed pedals

### Need for Speed: Most Wanted (2012)

This Criterion game is similar to their other games from this time in terms of
DirectInput usage.

1.  Hardware Effects Usage: Medium
2.  Requires Wheel: Without this, an inferior, fallback
    model meant for joysticks is used; many effects are missing and forces are
    applied along the Y axis.
3.  Weak steering forces: Especially on modern direct drive wheels with high torque.
    Use the `Spring Coefficient` in `FFFSake` to tune your experience.

> This game currently lists an incorrect fix on various online forums, a DLL replacement
that rotates forces.

### Race Room

> TODO: Game available but study pending

1.  FFB Crash: `HidHide` is needed to hide the problematic controller from the game, while
    using `vJoy` to play the game.

### Richard Burns' Rally

> TODO: Game available but study pending

### Test Drive Unlimited

> TODO: Game available but study pending

### Test Drive Unlimited 2

> TODO: Game available but study pending

### Tokyo Xtreme Racer

1.  FFB Crash: `HidHide` is needed to hide the problematic controller from the game, while
    using `vJoy` to play the game.
2.  (Unconfirmed) Requires Wheel: Otherwise no force feedback in game.

## Games with generally excellent implementations

The following games generally have excellent implementations and offer plenty of
input and FFB configuration in-game that they can be made to work with most wheels.

1.  Codemasters games after (approx) 2018: F1 games
2.  American Truck Simulator
3.  Euro Truck Simulator 2
4.  Probably most contemporary hard core racing sims

You should not need `FFFSake` and Joystick Gremlin for these games. However you could
still Joystick Gremlin (without `FFFSake`) to use your
[joystick as an H-shifter](../joystick_gremlin_plugins//h_shifter.md).
