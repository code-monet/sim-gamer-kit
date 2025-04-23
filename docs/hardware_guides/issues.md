[//]: # "© 2025 Code Monet <code.monet@proton.me>"

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

## (Racing Games) Controller Detected "not wheel"

This may not be obvious; one common sign is that some wheel configurations are
missing in game settings. Force feedback may be missing in some other games.

> If using racing wheels directly with the game, `IndirectInput` is needed to fix this.

> If using `vJoy`, see the [game guides](../game_guides/issues.md) on how to address this.

## Force Feedback causes game crash

Games can crash for many reasons, but this particular crash happens specifically
when a FFB device is plugged in, or FFB effects are enabled.
`FFFSake` with `Reducer` engine should fix this, unless the actual problem is
something else.

## Force Feedback causes (severe) FPS drop

See "Game Loop Blocked By Force Feedback Commands" in
[Game Issues](../game_guides/issues.md). Some controllers just take longer to
handle commands than others, and some games are not written to properly handle this.

## Force Feedback effects are incorrectly/incompletely implemented

Device manufacturers have some leeway in how detailed their implementation of
hardware effects is, and their simpler implementation may lead to an inferior
in-game experience. Unfortunately sometimes the manufacturer will also have bugs
in their implementation.

`FFFSake` with `Reducer` engine should fix this.
