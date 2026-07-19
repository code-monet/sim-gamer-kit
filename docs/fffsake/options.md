[//]: # "© 2026 Code Monet <code.monet@proton.me>"

# Configuration Options

FFFSake provides the following options, exposed via the Joystick Gremlin plugin.

Quickstart:

1. Set `FF Device Type` to match your device.
2. Select `FF Device` if you have multiple FFB devices connected.
3. Set `Device Gain %` to a comfortable value (recommend leaving hardware gain setting, via the vendor's control panel/app, at maximum).

Then, as you play specific games, you can visit the [game guides](../game_guides/index.md) for recommended settings and compatibility fixes.

---

## Engine Selection

Most people should use the `Reducer` engine. `Forwarder` will continue to be provided
for debugging purposes and to help understand game compatiblity issues not yet captured in the `Reducer` engine.

---

## Device Selection and Settings

Allows selecting the device, and setting device-global options.

| Option | Values | Description |
| :--- | :--- | :--- |
| `FF Device` | `First FFB Device`, <device 1>, ... | Which device to send force feedback commands to. |
| `FF Device Type` | `Wheel`, `Joystick` | (Reducer only) Whether the device is a FF wheel or joystick. |
| `Device Gain %` | `[0, 100]` | User gain setting for all effects. May have no effect with forwarding engine. |

---

### Gain Settings

Gains scale the intensity of individual force effects. On a per-game basis, these can be used to enhance certain effects, improve comfort, and in some cases, avoid saturating effects (leading to loss of fidelity/feedback). More details in the [game issues guide](../game_guides/issues.md).

Games typically use a subset of these, so changing them may not have an effect. The [game guides](../game_guides/index.md) have recommended settings for some games. Default value is 100%.

| Option | Values | Description |
| :--- | :--- | :--- |
| `Constant Gain %` | `[0, 300]` | Constant forces can be used for anything and everything. |
| `Ramp Gain %` | `[0, 300]` | Used for slow rise or fall effects. |
| `Sine Gain %` | `[0, 300]` | Used for uneven ground effects, aerodynamics, oscillation. |
| `Square Gain %` | `[0, 300]` | Used for gear grinding, stairs, rough terrain. |
| `Triangle Gain %` | `[0, 300]` | Used similar to square. |
| `Sawtooth Up Gain %` | `[0, 300]` | Ratcheting effects, weapon kick. |
| `Sawtooth Down Gain %` | `[0, 300]` | Used similar to sawtooth up. |
| `Spring Gain %` | `[0, 300]` | Used for counter steer, or to generally center the axes. |
| `Damper Gain %` | `[0, 300]` | Used to prevent oscillation, and provide a friction-like effect. |
| `Inertia Gain %` | `[0, 300]` | Used to emulate device internal friction - rarely used. |
| `Friction Gain %` | `[0, 300]` | Used to emulate device mass - rarely used. |

### Coefficient Multipliers

Coefficient multipliers adjust the feeling of effects that are typically tuned by hardware manufacturers; but since the
reducer engine re-implements these effects, we need to tune them ourselves.
Coefficient multipliers apply on top of other gains. Adjust gains if the effect feels weak all the time; adjust coefficients if the effect feels "wrong" or uneven.

| Option | Values | Description |
| :--- | :--- | :--- |
| `Spring Coefficient %` | `[0, 300]` | Tune to get sufficiently strong counter steer (in games that use spring for it) near the center of rotation. |
| `Friction Coefficient %` | `[0, 1000]` | Tune to get a good friction feeling (not too weak, but not too gritty/backlashing either). |

### Compatibility Options

Options to fix compatibility issues stemming from non-standard or buggy behavior in specific games.
Unless needed, these should be left to the default value.
See the [Game guides](../game_guides/index.md) for recommended settings.

| Option | Values | Description |
| :--- | :--- | :--- |
| `Compatibility: Restore minimized forces` | `True`, `False` | When certain forces are unintentionally zero, this will unminimize them. |
| `Compatibility: Force restart on update` | `True`, `False` | When the game expects certain forces to be restarted on each update. |

---

### Debugging Options

Most users shouldn't need to change these from their default values.

| Option | Values | Description |
| :--- | :--- | :--- |
| `Device Update Period (ms)` | `[1, 34]` | Device update period in milliseconds. |
| `Y-Axis Forces Handling` | `AUTO`, `ROTATE_TO_X` | How to handle Y-axis forces. |
