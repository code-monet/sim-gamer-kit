# FFFSake

> Through this document, FFB is used as an acronym for Force Feedback.

FFFSake, or **F**or **F**orce **F**eedback's **Sake**, is:

*   Technically, a
library that can bridge FFB commands received by vJoy to a
DirectInput compatible device.
*   Practically, a plugin to get FFB effects on your
physical device while your game is actually being played with a
vJoy virtual joystick, which is in turn being fed with inputs by an
application like Joystick Gremlin.

# What is this for?

> tl;dr if you're having a wheel/joystick binding, input or FFB
problem, Joystick Gremlin with FFFSake can usually help you work around that.

In a perfect world, your game controller (typically a racing wheel or
joystick/HOTAS, plus additional hardware like pedals, H-shifter etc.)
would allow configuring **inputs**. They would also correctly implement **outputs** i.e. the
[FFB
specification for DirectInput devices](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee417563(v=vs.85))
**completely** and **correctly**.

Meanwhile, the game you're playing would have a nice configurable control
scheme. They'd allow you to tune your FFB experience based on
your preferences and your specific hardware.

In the real world, both hardware and software can fail at these for a variety
of reasons. This is where third-party tools like Joystick Gremlin and vJoy come
in. You configure your game to use the vJoy virtual joystick as a FFB
capable input device, and use Joystick Gremlin to read control inputs from
various sources (say, your physical steering wheel), and "feed" them into the
vJoy virtual joystick. This allows you to fix a broad range of input-related
issues, such as:

1.  Setting response curves for analog axes, usually pedals.
2.  Configuring buttons and switches as toggle or sticky.
3.  Converting split pedals to combined or vice versa (for using modern racing pedals with flight sims or older racing games)
4.  Macro playback
5.  Combination inputs
6.  Mode switches

FFFSake handles the output i.e. FFB side of things, taking these commands
from the vJoy device (coming from the video game) and writing them to your physical
FFB capable device. In this process, it can also fix various force
feedback issues and allow some amount of tweaking; see the Features section later.

## Setup

> TODO: Add screenshot and links

FFFSake is currently offered as a (Python) plugin for Joystick Gremlin.
If you would like to integrate FFFSake into your application as a DLL,
please open a GitHub ticket.

Using FFFSake requires the following third party dependencies. First,
download them all:

1.  vJoy virtual joystick driver. Please download the latest signed
    driver from
    [Brunner Innovation's fork on GitHub](https://github.com/BrunnerInnovation/vJoy/releases). Download both the setup executable as well as the SDK zip archive.
2.  [Joystick Gremlin](https://whitemagic.github.io/JoystickGremlin/)
3.  (Strongly Recommended) [HidHide](https://github.com/nefarius/HidHide/releases),
    a kernel-mode filter driver to hide physical devices from games.

Install and configure these; a nice detailed guide is available in the
Joystick Gremlin link. Short version:

1.  Install vJoy and reboot.
2.  Install HidHide and reboot.
3.  Install Joystic Gremlin, or use the "portable" version.
4.  Launch the vJoy Control Panel from the Start Menu and configure it. The
    recommendation on Joystick Gremlin is a bit outdated, instead, I suggest
    having it match the screenshot below.
5.  Launch and configure Joystick Gremlin. Suggestion for new users:
    1.   Verify that your plugged in physical device shows up; switch to
         that tab. From the `Actions` menu, create a 1:1 mapping. Scroll down
         the list and verify that a sensible mapping was created (usually works
         as long as you start with a clean slate i.e. zero existing mappings).
    2.   Switch to the plugins tab. Use the `Add plugin` button and browse to
         the `fffsake.py` (not `fffsake.pyd`!) file.
    3.   Once the plugin has been added, from the `Output Device` dropdown in
         plugin configuration, select your FFB capable device. Most
         people would have exactly one such device.
    4.   Select either the `forwarding` or the `reducing` engine. See section
         below for details. If you're not sure, start with the `reducing` engine.
    5.   Save the profile.
6.  Launch and configure HidHide:
    1.   Decide if you want to use list all the games you want to use with vJoy
         (**allowlist**, "Inverse cloak" unchecked), or list all the games and
         applications you won't be using with vJoy (**blocklist**,
         "Inverse cloak" checked). I use the former because that list is shorter
         for me.
    2.   Add paths to all the applications that belong to the above list. For
         games with launchers, you want the game binary path, not the launcher.
         I typically launch the application, and then use the Windows Task
         Manager to find the path of the application `.exe` file.
         1.   If using an **allowlist**, make sure to add paths to Joystick
              Gremlin as well as the control panel/configuration application
              for your physical device.
    3.   On the devices tab, select the physical device (needs to be plugged
         in to show up) that you want to use through Joystick Gremlin.
    4.   Check "Enable filtering" and unplug-replug (or power off/on) the
         device.
7.  Go back to Joystick Gremlin, ensure that your physical device is still there.
    If not, double check that you added the Joystick Gremlin application path
    correctly (for your chosen scheme, allowlist or blocklist). Then click on
    "Enable" button.

This is a lot of setup, if you made it this far, congratulations! You've
enabled some really powerful tools for your sim gaming journey.

## Usage

Once you've completed the above setup, future setup involves:

1.  Launching HidHide and ensuring the filter is enabled.
2.  Launch Joystick Gremlin and load your desired profile. Click on "Enable".

At this point you can launch your game and configure it for vJoy. You should be
able to select and configure it inside the game as you would any other
device.

### FFFSake Features

#### Common Features

Both engines have the following features:

1.  Incorrect rotation of effects (but also see
    [Indirect Input](../indirect_input/index.md))
2.  FFB commands issued faster than the device can handle them, usually leading
    to a drop in FPS in game when using a FFB device.
3.  Setting gain for individual hardware effects
    (NOTE: targeted for a future release).

#### Forwarding Engine

The forwarding engine takes FFB commands received from vJoy (coming from
the game or from Windows) and writes them to the physical device using DirectInput.
In this process, the above compatibility fixes are also applied.

#### Reducing Engine

The reducing engine takes FFB commands received from vJoy (coming from
the game or from Windows) and "reduces" them to a stream of constant forces, which
are written to the physical device using DirectInput. This way the above common and
following additional compatibility issues can be fixed:

1.  Incorrect [hardware effects](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee417541(v=vs.85))
    in the physical device. See also
    [types of FFB issues](../game_guides/issues.md).

## Limitations and Known Issues

The following limitations exist because I don't know of any gamers who are affected by
them; if you are, please in touch via
[GitHub Discussions](https://github.com/code-monet/sim-gamer-kit/discussions)

1.  Only one vJoy device is supported.
2.  Only one FFB axis devices are supported in the reducing engine. In other
    words, it's only expected to be used for racing wheels. I don't know of any
    FFB joysticks that have mistakes in their hardware effects implementation.

The following known issues will be addressed in a future release:

1.  High CPU usage, especially from the reducing engine.
2.  Only one FFB axis devices are supported in the forwarding engine. In other
    words, it's only expected to be used for racing wheels. It's relatively easy to
    add support for (two axes) FFB joysticks, it's just currently lower
    priority given how rare such devices are.

## Troubleshooting

Section to be filled out based on user experience. Please share yours via the
[GitHub Discussions](https://github.com/code-monet/sim-gamer-kit/discussions) page!