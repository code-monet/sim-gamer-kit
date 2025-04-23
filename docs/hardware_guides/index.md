[//]: # "© 2025 Code Monet <code.monet@proton.me>"

# Hardware Guides

This guide captures known compatibility issues with controllers I have
myself tried, or that have been reported by users. Please contribute via
[GitHub Discussions](https://github.com/code-monet/sim-gamer-kit/discussions)!

See also: list of common [issues](./issues.md).

## Thrustmaster

### Thrustmaster TMX

This device is likely on "stable" software.

#### Known Compatibility Problems

The wheel software is generally really good. Compatibility issues can arise from
a somewhat strict implementation of the PID spec:

1.  Some effects can be missing in certain games because this wheel will
    reject FFB effects with parameters out of spec (usually axis rotation).
    Seen in Burnout Paradise.

Issue can be fixed either with `FFFSake` or `IndirectInput`.

#### Configurability

General:

1.   Game-specific profiles are *not* available.
2.   User-selected profiles are *not* available either.

Inputs:

1.   Axes dead zones can be set.
2.   Axes curves cannot be set.
3.   Combined vs Split pedals can be set.
4.   Buttons cannot be mapped to system actions, macros, or keyboard input.

Force Feedback:

1.   Spring control by game vs wheel can be set (set to game)
2.   Hardware effect strengths can be set in limited, slightly confusing ways.

## TurtleBeach

### TurtleBeach Velocity One Race

As of this writing, TurtleBeach has promised a new firmware with some fixes.

#### Known Compatibility Problems

With system firmware version 1.4.0, any of the [described issues](../game_guides/issues.md)
can kick in for games not in their list of official supported games e.g.

1.  Crew Motorfest game crash
2.  Crew 2 FPS drop
3.  Incorrect FFB in most Need for Speed games.
4.  Inability to combine or zero pedals and analog paddles

The wheel is also detected as "not a wheel" by some games, and a subset of these games
then use a different FFB logic meant as a fallback. Usually
this results in missing or weak FFB (e.g. Need for Speed Most Wanted 2012,
Bus Simulator 21). In `The Crew 2`, wheel configuration is disabled in the settings menu.

This wheel also presents a dud "Slider" axis that doesn't map to a physical axis, and
is unfortunately not zeroed. Usually a game where this is an issue will need you
to use Joystick Gremlin with `FFFSake` anyway, to combine/zero pedals.

Fixing issues usually requires `FFFSake` with the `Reducer` engine, and sometimes
also needs `IndirectInput`. Combined pedals can be achieved using Joystick Gremlin.
Dud axes can be hidden or zeroed using Joystick Gremlin.

#### Configurability

General:

1.   Game-specific profiles are *not* available.
2.   User-selected profiles are available - 10 slots via on-device memory.

Inputs:

1.   Axes dead zones can be set.
2.   Axes curves can be selected from (slightly confusing) "sensitivity" presets.
     These probably adjust non-linearity of the inputs.
     1.   Clutch pedals now have "bite point" setting.
3.   Combined vs Split pedals *cannot* be set.
4.   Buttons can be mapped to some system actions
     1.   Volume up/down/mute
     2.   TODO: Complete this.
5.   Buttons cannot be mapped to macros, or keyboard input.

Force Feedback:

1.   Spring control by game vs wheel *cannot* be set.
2.   Effect strengths can only be set for:
     1.   Spring - unsure when this applies.
     2.   Damper - unsure if this overrides game settings.
