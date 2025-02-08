# Driving and Flight Games Input/Force Feedback Guide

## How to use this guide

First, check the list of games below and see if it already has the game you're
looking for.

If not, check the list of [controllers](../hardware_guides/index.md). This
is currently a very short list; you can help fill it out! Get in touch via
[GitHub Discussions](https://github.com/code-monet/sim-gamer-kit/discussions)

Then check the list of [issues](./issues.md) to see if one or more matches what
you are seeing. Try the suggested fixes and please share your experience via
[GitHub Discussions](https://github.com/code-monet/sim-gamer-kit/discussions)
so I can update this doc.

## Games With Known Compatibility Issues

The following short forms are used to refer to common [issues](./issues.md):

*   Slip: FFB commands slippage fix is needed via FFFSake
*   Combined pedals: An axis (usually accelerator and brake pedals) need to be
    combined into a single axis.
*   Zeroed pedals: An axis needs to be zeroed. Pedals and analog paddles on
    modern wheels are usually not zeroed.
*   Hardware Effects Usage: This can help explain why a game might not feel
    right on your force feedback device if the latter doesn't implement built-in
    effects properly. A rating is given out of:
    *   High: The game uses a lot of hardware FFB effects, and uses them in
        advanced ways.
    *   Medium: The game uses some hardware FFB effects in simple ways.
    *   Minimal: The game uses only constant and damper forces, the latter in
        very simple ways.
    *   None: The game only uses constant forces.
*   FFB high effect count: This game uses a large-ish number of FFB effects and
    is known to crash or lose effects with some wheels.
*   Indirect Input: The game needs the listed feature from
    [Indirect Input](../indirect_input/index.md)

### Burnout Paradise

Also applies to the Remastered and Ultimate Box versions. This Criterion game has
some of the same issues from other Criterion racing games from this time:

1.  Hardware Effects Usage: Medium
2.  Indirect Input: Forced wheel detection

### Bus Simulator 21

A curious driving that uses Unreal Engine, which may be to blame for compatibility
issues with FFB wheels:

1.  Indirect Input: Forced wheel detection

> TODO: Game needs further study

### Crew 2

This game supports joystick, HOTAS and racing wheels. Known compatibility issues:

1.  Slip
2.  Hardware Effects Usage: Medium

### Crew Motorfest

All the same issues as Crew 2, as well as:

1.  FFB high effect count (crash to desktop)

### Dirt 3

One of Codemaster's earlier games before they got really good with racing wheels.

1.  Indirect Input
    1.   Forced wheel detection
    2.   Vendor spoof (only for H-shifters not made by a manufacturer in their hard-coded list)

### Dirt Rally

> TODO: Game available but study pending

### Dirt Rally 2.0

> TODO: Game available but study pending

### Elite: Dangerous

Only the first 32 buttons can be mapped from a single controller. Hmm, we wonder
[where that limit comes from](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee416627(v=vs.85)). Players will use vJoy and Joystick Gremlin to map
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

### Need for Speed: Heat

One of the few racing games I have seen that simply doesn't allow you to bind
controls!

1.  Inability to bind controls. Use Joystick Gremlin and bind as follows:
    1.   TODO Fill this section
2.  Zeroed pedals
3.  TODO: Fill out FFB information

### Need for Speed: Hot Pursuit (2010)

This Criterion game has some of the same issues from other Criterion racing games
from this time:

1.  Hardware Effects Usage: Medium
2.  Indirect Input: Forced wheel detection
3.  Zeroed pedals

### Need for Speed: Most Wanted (2012)

This Criterion game has some of the same issues from other Criterion racing games
from this time:

1.  Hardware Effects Usage: Medium
2.  Indirect Input: Forced wheel detection

> This game currently lists an incorrect fix on various online forums, a DLL replacement
that rotates forces. With that fix, you get a fallback FFB model meant for joysticks.

### Richard Burns' Rally

> TODO: Game available but study pending

### Test Drive Unlimited

> TODO: Game available but study pending

### Test Drive Unlimited 2

> TODO: Game available but study pending

## Games with generally good compatibility

1.  Codemasters games after (approx) 2018: F1 games
2.  American Truck Simulator
3.  Euro Truck Simulator 2