# Sim Gamer Kit - vJoy Mods

## vJoyConf.exe

This directory currently has a single tool - `bin\vJoyConf.exe`. You can simply run it; it requires
privilege elevation as it needs to modify the `vJoy` kernel drivers. It ships with `vJoy`, but
this one includes some additional features and fixes:

1.  Ability to configure the `vJoy` device to show up as a wheel to `DirectInput`.

...that's it for now.

### Installation

You can replace the binary that shipped with `vJoy` and is installed on your system (likely at
`C:\Program Files\vJoy\x64`) with this one.

### Background

Creating a new build of vJoy requires going through a (somewhat) expensive process of driver and
app signing. It is not likely that we'll see a new release of `vJoy`, so this kit includes updated
versions. The app does not require signing to work.

### Building yourself

You can build this binary yourself from [my fork of `vJoy`](https://github.com/code-monet/vJoy).
As of writing, the necessary changes are in the `usage_pages` branch. If that branch no longer exists,
check the `main` branch.
