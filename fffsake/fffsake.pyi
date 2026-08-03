import enum


def DetectFfbDevices(vendor_id: int = 0, product_id: int = 0) -> list[ExtendedDeviceInfo]:
    """
    Enumerate all DirectInput devices that support force feedback. Returns a list of ExtendedDeviceInfo.
    """

def DetectGameControllers(vendor_id: int = 0, product_id: int = 0) -> list[ExtendedDeviceInfo]:
    """
    Enumerate all game controllers currently connected to the system. Returns a list of ExtendedDeviceInfo.
    """

class DeviceOptions:
    def __init__(self) -> None: ...

    DEVICE_GAIN_MAX: float = ...
    """(arg: object, /) -> float"""

    GAIN_MIN: float = ...
    """(arg: object, /) -> float"""

    GAIN_NOMINAL: float = ...
    """(arg: object, /) -> float"""

    GAIN_MAX: float = ...
    """(arg: object, /) -> float"""

    COEFFICIENT_MULTIPLIER_MIN: float = ...
    """(arg: object, /) -> float"""

    COEFFICIENT_MULTIPLIER_NOMINAL: float = ...
    """(arg: object, /) -> float"""

    COEFFICIENT_MULTIPLIER_MAX: float = ...
    """(arg: object, /) -> float"""

    def set_device_gain(self, gain: float) -> None:
        """Set the overall device gain. Allowed range: [0, 5.0]."""

    def set_constant_gain(self, gain: float) -> None:
        """Set the gain applied to constant force effects."""

    def set_ramp_gain(self, gain: float) -> None:
        """Set the gain applied to ramp force effects."""

    def set_sine_gain(self, gain: float) -> None:
        """Set the gain applied to sine periodic effects."""

    def set_square_gain(self, gain: float) -> None:
        """Set the gain applied to square periodic effects."""

    def set_sawtooth_up_gain(self, gain: float) -> None:
        """Set the gain applied to sawtooth-up periodic effects."""

    def set_sawtooth_down_gain(self, gain: float) -> None:
        """Set the gain applied to sawtooth-down periodic effects."""

    def set_triangle_gain(self, gain: float) -> None:
        """Set the gain applied to triangle periodic effects."""

    def set_spring_gain(self, gain: float) -> None:
        """Set the gain applied to spring condition effects."""

    def set_damper_gain(self, gain: float) -> None:
        """Set the gain applied to damper condition effects."""

    def set_inertia_gain(self, gain: float) -> None:
        """Set the gain applied to inertia condition effects."""

    def set_friction_gain(self, gain: float) -> None:
        """Set the gain applied to friction condition effects."""

    def set_spring_coefficient_multiplier(self, multiplier: float) -> None:
        """Set the multiplier applied to spring condition coefficients."""

    def set_friction_coefficient_multiplier(self, multiplier: float) -> None:
        """Set the multiplier applied to friction condition coefficients."""

    def compat_e_uprest(self) -> bool:
        """
        Check if compat mode is enabled: force updates also restart the effect.
        """

    def set_compat_e_uprest(self, enabled: bool) -> None:
        """
        Enable/disable compat mode: force updates also restart the effect. Primarily affects periodic forces.
        """

    def compat_unminimize_forces(self) -> bool:
        """Check if compat mode is enabled: maximize forces that are muted."""

    def set_compat_unminimize_forces(self, enabled: bool) -> None:
        """Enable/disable compat mode: maximize forces that are muted."""

    def compat_unminimize_conditions(self) -> bool:
        """Check if compat mode is enabled: unminimize conditions that are muted."""

    def set_compat_unminimize_conditions(self, enabled: bool) -> None:
        """Enable/disable compat mode: unminimize conditions that are muted."""

class ExtendedDeviceInfo:
    def __init__(self) -> None: ...

    def __str__(self) -> str: ...

    @property
    def guid(self) -> GUID:
        """DirectInput device GUID."""

    @property
    def name(self) -> str:
        """Human-readable device name."""

    @property
    def vendor_id(self) -> int:
        """USB Vendor ID."""

    @property
    def product_id(self) -> int:
        """USB Product ID."""

    @property
    def axes(self) -> int:
        """Number of axes available on the device."""

    @property
    def buttons(self) -> int:
        """Number of buttons available on the device."""

    @property
    def hats(self) -> int:
        """Number of POV hats available on the device."""

    @property
    def x_is_ffb(self) -> bool:
        """True if the X-axis supports force feedback."""

    @property
    def y_is_ffb(self) -> bool:
        """True if the Y-axis supports force feedback."""

    @property
    def is_virtual(self) -> bool:
        """True if the device is a virtual vJoy device."""

class FfbEngineType(enum.Enum):
    """Specifies the type of force feedback engine to use."""

    FORWARDER = 0
    """Direct 1:1 force feedback forwarding."""

    REDUCER_1D = 1
    """1D force reducer engine (for steering wheels)."""

    REDUCER_2D = 2
    """2D force reducer engine (for joysticks)."""

def FffsakeCleanup() -> None:
    """Performs cleanup for FFFSake, if active"""

class FffsakeOptions:
    def __init__(self) -> None: ...

    DEFAULT_DEVICE_UPDATE_PERIOD_MS: int = ...
    """(arg: object, /) -> int"""

    MIN_DEVICE_UPDATE_PERIOD_MS: int = ...
    """(arg: object, /) -> int"""

    MAX_DEVICE_UPDATE_PERIOD_MS: int = ...
    """(arg: object, /) -> int"""

    @property
    def device_options(self) -> DeviceOptions:
        """Engine-level gain and compatibility options."""

    @device_options.setter
    def device_options(self, arg: DeviceOptions, /) -> None: ...

    @property
    def y_forces_handling(self) -> YForcesHandling:
        """Controls how forces meant for the Y axis are handled."""

    @y_forces_handling.setter
    def y_forces_handling(self, arg: YForcesHandling, /) -> None: ...

    def device_update_period_ms(self) -> int:
        """Get the device update period in milliseconds."""

    def set_device_update_period_ms(self, update_period_ms: int) -> None:
        """Set the device update period in milliseconds. Allowed range: [1, 34]."""

class GUID:
    def __init__(self) -> None: ...

def GetVersionMismatchMessage() -> str | None:
    """
    Returns a version mismatch message if the vJoy DLL and driver versions differ, otherwise returns None.
    """

def IsFffsakeActive() -> int:
    """Returns true if FFFSake is active"""

def IsVjoyConfigFull(device_id: int = 1) -> bool:
    """
    Check if the specified vJoy device exists and is configured with full controls (8 axes, 128 buttons, 4 POV hats).
    """

def IsVjoyDevice(arg: ExtendedDeviceInfo, /) -> bool:
    """Check if an ExtendedDeviceInfo represents a virtual vJoy device."""

def RegisterFffsakeForwarder(device_guid: GUID) -> int:
    """Register the FFFSake forwarder engine for the given device GUID."""

def RegisterFffsakeReducer(device_guid: GUID, device_type: UserReportedDeviceType) -> int:
    """
    Register the FFFSake reducer engine for the given device GUID and user reported device type. Returns False if the device is not FFB-capable.
    """

def SetFffsakeOptions(arg: FffsakeOptions, /) -> int:
    """Sets FFFSake options. Returns False if FFFSake is not active"""

class UserReportedDeviceType(enum.Enum):
    """Allows the user to specify the actual device type."""

    FFB_JOYSTICK = 0

    FFB_WHEEL = 1

class VjoyFfbController:
    """
    Controller class to forward inputs from a physical game controller to vJoy and handle force feedback.
    """

    def __init__(self) -> None: ...

    def Activate(self, device_guid: GUID, engine_type: FfbEngineType) -> bool:
        """
        Activate input forwarding and FFB engine from the physical device with the given GUID.
        """

    def Deactivate(self) -> None:
        """
        Deactivate input forwarding and FFB engine, releasing the acquired vJoy device.
        """

    def IsActive(self) -> bool:
        """Check if input forwarding is currently active."""

    def SetOptions(self, options: FffsakeOptions) -> None:
        """Set runtime options for the controller."""

    @property
    def options(self) -> FffsakeOptions:
        """Get current runtime options for the controller."""

class YForcesHandling(enum.Enum):
    """Controls how forces meant for the Y axis are handled."""

    AUTO = 0

    ROTATE_TO_X = 1
