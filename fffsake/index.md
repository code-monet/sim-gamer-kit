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

Currently only an x86 Python pre-compiled module is offered, since Joystick Gremlin
is expected to be the only way people use it. If you're a developer interested in
x64 builds or a DLL, please open a GitHub ticket.
