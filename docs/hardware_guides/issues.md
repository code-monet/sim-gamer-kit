# Hardware Issues and Workarounds

A list of common limitations or bugs in DirectInput hardware and how to work around them.

## No user profiles

If the device control panel/app does not support user profiles, Joystick Gremlin can
instead be used to create profiles, saved on/loaded from your computer.

## Cannot combine or zero pedals

Joystick Gremlin can be used to combine pedals (`Combine pedals` option in the
`Actions` menu). Separate but zeroed pedals can be achieved by creating a
`curve` mapping.

## Cannot configure pedal/paddle curves (enough)

Joystick Gremlin can be used to set custom arbitrary curves for pedals and other
analog axes.

## Detected as joystick

This may not be obvious; one common sign is that some wheel configurations are
missing in game settings. Force feedback may be missing in some other games.
`IndirectInput` is needed to fix this.

## Force Feedback causes game crash

Games can crash for many reason, but this particular crash happens specifically
when a FFB device is plugged in, or FFB effects are enabled.
`FFFSake` with `Reducer` engine should fix this, unless the actual problem is
something else.

## Force Feedback causes (severe) FPS drop

See "Game Loop Blocked By Force Feedback Commands" in
[Game Issues](../game_guides/issues.md). While technically the controller is
guilty for blocking excessively on commands, ultimately this is something the
game developer should anticipate and handle.

## Force Feedback effects are incorrectly/incompletely implemented

Device manufacturers have some leeway in how detailed their implementation of
hardware effects is, and their simpler implementation may lead to an inferior
in-game experience. Unfortunately sometimes the manufacturer will also have bugs
in their implementation.

`FFFSake` with `Reducer` engine should fix this.
