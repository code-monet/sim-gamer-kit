[//]: # "© 2025 Code Monet <code.monet@proton.me>"

# FFFSake

See setup docs for usage. The rest of this doc is intended for
developers or debugging crashes.

This version of `FFFSake` was compiled using MSVC 17.12.3 and
needs an equal or newer
[runtime](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)

It also needs the `vJoyInterface.dll` file for the right architecture and
a "matching" version. This release was tested against the
[2.2.2.0 release](https://github.com/BrunnerInnovation/vJoy); newer releases
should work, older releases might work.

Compiled Python extensions need to match the architecture and version of the interpreter;
the offered extensions are for Joystick Gremlin:
1.  R13: x86, Python 3.6
2.  R14: x64, Python 3.13

If you're a developer interested in other builds or a DLL, please open a GitHub ticket.
