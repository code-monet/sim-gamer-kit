# FFFSake Setup with Joystick Gremlin R14

Budget about 15 minutes for this one-time setup.

Using FFFSake requires the following third party dependencies. First,
download them all:

1.  vJoy virtual joystick driver. Please download the latest signed
    driver from
    [Brunner Innovation's fork on GitHub](https://github.com/BrunnerInnovation/vJoy/releases). Download both the setup executable as well as the `SDK.zip` archive.
2.  [My fork of Joystick Gremlin](https://github.com/code-monet/JoystickGremlin/releases)
3.  (Strongly Recommended) [HidHide](https://github.com/nefarius/HidHide/releases),
    a kernel-mode filter driver to hide physical devices from games. You
    will probably have a lot of trouble configuring your game to use vJoy,
    or using `FFFSake`, if you don't hide the physical device redirected through
    vJoy from the game. HidHide is the best option, at the time of this writing.

Install and configure these:

1.  Install vJoy. You can skip the reboot, doing it after the next step.
2.  Install HidHide and reboot.
3.  Extract Joystick Gremlin to a directory of your choice.
4.  Launch the `Configure vJoy` app from the Start Menu and configure vJoy. The
    recommendation on the Joystick Gremlin page is a bit outdated; instead,
    I suggest following [this guide](vjoy_configuration.md) if you play mostly driving games.
    For everyone else, the recommended default is:

![vJoy Configuration!](../resources/vjoy_conf.png)

5.  Plug in your FFB device, then launch and configure Joystick Gremlin:
    1.   Suggestion for new users: verify that your plugged in physical device shows
         up; switch to that tab. From the `Actions` menu, create a 1:1 mapping. Scroll down
         the list and verify that a 1:1 mapping was created (usually works
         as long as you start with a clean slate i.e. zero existing mappings).
    2.   Switch to the `Scripts` tab. Use the `Add Script` button and browse to
         the `joystick_gremlin\_internal\user_scripts\fffsake.py` file,
         at the location you extracted Joystick Gremlin to.
    3.   Once the plugin has been added, click on the cog wheel for the plugin to
         open its configuration. From the `FF Device` dropdown in
         plugin configuration, ensure your FFB capable device is selected. Most
         people would have exactly one such device.
    4.   Select either the `forwarder` or the `reducer` engine. See section
         below for details. If you're not sure, start with the `reducer` engine
         if using a wheel and `forwarder` if using a joystick.
    5.   Bind a button for `Mute/Unmute Force Feedback`. Think of this as a safety cutoff
         button, to be pressed if you lose control of your FFB device. For this reason, use a button
         not on the FFB joystick/wheel rim. It doesn't need to be on the FFB device either.
         Once done, the plugin page should look something like follows: ![FFFSake Plugin!](../resources/fffsake_gremlin_plugin_r14.png)
    6.   Save the profile.
    7.   Close Joystick Gremlin for the next step.
6.  Launch and
    [configure HidHide](https://github.com/nefarius/HidHide?tab=readme-ov-file#user-guide):
    1.   Decide if you want to use list all the games you want to use with vJoy
         (**allowlist**, "Inverse cloak" unchecked), or list all the games and
         applications you won't be using with vJoy (**blocklist**,
         "Inverse cloak" checked). I use the blocklist because that list is shorter
         for me.
    2.   Add paths to all the applications that belong to the above list. For
         games with launchers, you want the game binary path, not the launcher.
         I typically launch the game, and then use Windows Task
         Manager (launch via `Ctrl + Shift + Esc`) to find the path of the
         application `.exe` file. The applications tab should look something like:
         ![HidHide Application Configuration for blocklist!](../resources/hid_hide_apps.png)
         1.   If using an **allowlist**, make sure to add paths to Joystick
              Gremlin as well as the control panel/configuration application
              for your physical device.
    3.   On the devices tab, select the physical device (needs to be plugged
         in to show up) that you want to use through Joystick Gremlin.
    4.   Check "Enable filtering" and unplug-replug (or power off/on) the
         device.
         ![HidHide Devices!](../resources/hid_hide_devices.png)
7.  Launch Joystick Gremlin, ensure that your physical device is still there.
    If not, double check that you added the Joystick Gremlin application path
    correctly (if you're using the allowlist approach) in HidHide. Then click on
    "Enable" button.

This is a lot of setup; if you made it this far, congratulations! You've
enabled some really powerful tools for your sim gaming journey. I suggest starting
with a single Joystick Gremlin profile and then branching out to more as you gain
experience with these tools.