"""Python wrapper for fffsake"""

import enum
from typing import Final, overload


class VjoyError(RuntimeError):
    """Base exception for all vJoy errors."""

class VjoyDriverNotEnabledError(VjoyError):
    """Raised when the vJoy driver is not enabled."""

class VjoyDeviceAcquireError(VjoyError):
    """Raised when acquiring the vJoy device fails."""

class FffsakeControllerError(RuntimeError):
    """Base exception for FFFSake controller errors."""

class ControllerAlreadyActiveError(FffsakeControllerError):
    """Raised when activating a controller that is already active."""

class BackendCreationError(FffsakeControllerError):
    """Raised when backend creation fails."""

class GUID:
    """Globally Unique Identifier (GUID) class."""

    @overload
    def __init__(self) -> None:
        """Initialize a new zeroed GUID."""

    @overload
    def __init__(self, guid_str: str) -> None:
        """
        Create a GUID from a string (e.g. "{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}").

        Raises RuntimeError if guid_str cannot be parsed.
        """

    def __eq__(self, arg: GUID, /) -> bool: ...

    def __ne__(self, arg: GUID, /) -> bool: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __hash__(self) -> int: ...

class DeviceOptions:
    def __init__(self) -> None: ...

    DEVICE_GAIN_MAX: Final[float] = ...
    """(arg: object, /) -> float"""

    GAIN_MIN: Final[float] = ...
    """(arg: object, /) -> float"""

    GAIN_NOMINAL: Final[float] = ...
    """(arg: object, /) -> float"""

    GAIN_MAX: Final[float] = ...
    """(arg: object, /) -> float"""

    COEFFICIENT_MULTIPLIER_MIN: Final[float] = ...
    """(arg: object, /) -> float"""

    COEFFICIENT_MULTIPLIER_NOMINAL: Final[float] = ...
    """(arg: object, /) -> float"""

    COEFFICIENT_MULTIPLIER_MAX: Final[float] = ...
    """(arg: object, /) -> float"""

    def set_device_gain(self, gain: float) -> None:
        """
        Set the overall device gain. Allowed range: [0, 1.0].

        Raises ValueError if gain is outside [0, 1.0].
        """

    def set_constant_gain(self, gain: float) -> None:
        """
        Set the gain applied to constant force effects. Allowed range: [0, 5.0].

        Raises ValueError if gain is outside [0, 5.0].
        """

    def set_ramp_gain(self, gain: float) -> None:
        """
        Set the gain applied to ramp force effects. Allowed range: [0, 5.0].

        Raises ValueError if gain is outside [0, 5.0].
        """

    def set_sine_gain(self, gain: float) -> None:
        """
        Set the gain applied to sine periodic effects. Allowed range: [0, 5.0].

        Raises ValueError if gain is outside [0, 5.0].
        """

    def set_square_gain(self, gain: float) -> None:
        """
        Set the gain applied to square periodic effects. Allowed range: [0, 5.0].

        Raises ValueError if gain is outside [0, 5.0].
        """

    def set_sawtooth_up_gain(self, gain: float) -> None:
        """
        Set the gain applied to sawtooth-up periodic effects. Allowed range: [0, 5.0].

        Raises ValueError if gain is outside [0, 5.0].
        """

    def set_sawtooth_down_gain(self, gain: float) -> None:
        """
        Set the gain applied to sawtooth-down periodic effects. Allowed range: [0, 5.0].

        Raises ValueError if gain is outside [0, 5.0].
        """

    def set_triangle_gain(self, gain: float) -> None:
        """
        Set the gain applied to triangle periodic effects. Allowed range: [0, 5.0].

        Raises ValueError if gain is outside [0, 5.0].
        """

    def set_spring_gain(self, gain: float) -> None:
        """
        Set the gain applied to spring condition effects. Allowed range: [0, 5.0].

        Raises ValueError if gain is outside [0, 5.0].
        """

    def set_damper_gain(self, gain: float) -> None:
        """
        Set the gain applied to damper condition effects. Allowed range: [0, 5.0].

        Raises ValueError if gain is outside [0, 5.0].
        """

    def set_inertia_gain(self, gain: float) -> None:
        """
        Set the gain applied to inertia condition effects. Allowed range: [0, 5.0].

        Raises ValueError if gain is outside [0, 5.0].
        """

    def set_friction_gain(self, gain: float) -> None:
        """
        Set the gain applied to friction condition effects. Allowed range: [0, 5.0].

        Raises ValueError if gain is outside [0, 5.0].
        """

    def set_spring_coefficient_multiplier(self, multiplier: float) -> None:
        """
        Set the multiplier applied to spring condition coefficients. Allowed range: [0, 5.0].

        Raises ValueError if multiplier is outside [0, 5.0].
        """

    def set_friction_coefficient_multiplier(self, multiplier: float) -> None:
        """
        Set the multiplier applied to friction condition coefficients. Allowed range: [0, 5.0].

        Raises ValueError if multiplier is outside [0, 5.0].
        """

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

class YForcesHandling(enum.Enum):
    """Controls how forces meant for the Y axis are handled."""

    AUTO = 0

    ROTATE_TO_X = 1

class UserReportedDeviceType(enum.Enum):
    """Allows the user to specify the actual device type."""

    FFB_JOYSTICK = 0

    FFB_WHEEL = 1

class FffsakeOptions:
    def __init__(self) -> None: ...

    DEFAULT_DEVICE_UPDATE_PERIOD_MS: Final[int] = ...
    """(arg: object, /) -> int"""

    MIN_DEVICE_UPDATE_PERIOD_MS: Final[int] = ...
    """(arg: object, /) -> int"""

    MAX_DEVICE_UPDATE_PERIOD_MS: Final[int] = ...
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
        """
        Set the device update period in milliseconds. Allowed range: [1, 34].

        Raises ValueError if update_period_ms is outside [1, 34].
        """

def GetVersionMismatchMessage() -> str | None:
    """
    Returns a version mismatch message if the vJoy DLL and driver versions differ, otherwise returns None.
    """

def SetFffsakeOptions(arg: FffsakeOptions, /) -> int:
    """Sets FFFSake options. Returns False if FFFSake is not active"""

def IsFffsakeActive() -> int:
    """Returns true if FFFSake is active"""

def FffsakeCleanup() -> None:
    """Performs cleanup for FFFSake, if active"""

class InstanceInfo:
    """Information about a DirectInput device instance."""

    def __init__(self) -> None: ...

    @property
    def guid_instance(self) -> GUID:
        """GUID of the device instance."""

    @property
    def guid_product(self) -> GUID:
        """GUID of the device product."""

    @property
    def device_type(self) -> int:
        """Device main type code."""

    @property
    def device_sub_type(self) -> int:
        """Device sub type code."""

    @property
    def vendor_id(self) -> int:
        """USB Vendor ID."""

    @property
    def product_id(self) -> int:
        """USB Product ID."""

    @property
    def instance_name(self) -> str:
        """Friendly name of the device instance."""

    @property
    def product_name(self) -> str:
        """Friendly name of the device product."""

class Capabilities:
    """Details about DirectInput device capabilities."""

    def __init__(self) -> None: ...

    def force_feedback(self) -> bool:
        """True if the device supports force feedback."""

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
    def device_type(self) -> int:
        """Device (category-level) type code."""

    @property
    def device_sub_type(self) -> int:
        """Device (sub-category) type code."""

class ExtendedDeviceInfo:
    """Information about a detected device."""

    def __init__(self) -> None:
        """Initialize a new ExtendedDeviceInfo object."""

    def __str__(self) -> str: ...

    @property
    def instance_info(self) -> InstanceInfo:
        """InstanceInfo of the device."""

    @property
    def capabilities(self) -> Capabilities:
        """Capabilities of the device."""

    @property
    def x_is_ffb(self) -> bool:
        """True if the X axis supports force feedback."""

    @property
    def y_is_ffb(self) -> bool:
        """True if the Y axis supports force feedback."""

def DetectFfbDevices(vendor_id: int = 0, product_id: int = 0) -> list[ExtendedDeviceInfo]:
    """
    Enumerate all DirectInput devices that support force feedback. Returns a list of ExtendedDeviceInfo.

    Raises RuntimeError if DirectInput initialization or device enumeration fails.
    """

def DetectGameControllers(vendor_id: int = 0, product_id: int = 0) -> list[ExtendedDeviceInfo]:
    """
    Enumerate all game controllers currently connected to the system. Returns a list of ExtendedDeviceInfo.

    Raises RuntimeError if DirectInput initialization or device enumeration fails.
    """

def IsVjoyDevice(arg: ExtendedDeviceInfo, /) -> bool:
    """Check if an ExtendedDeviceInfo represents a virtual vJoy device."""

def IsWheelDevice(arg: ExtendedDeviceInfo, /) -> bool:
    """Check if an ExtendedDeviceInfo represents a driving wheel device."""

def RegisterFffsakeReducer(device_guid: GUID, device_type: UserReportedDeviceType) -> int:
    """
    Register the FFFSake reducer engine for the given device GUID and user reported device type. Returns False if the device is not FFB-capable.

    Raises RuntimeError if DirectInput initialization fails.
    """

def RegisterFffsakeForwarder(device_guid: GUID) -> int:
    """
    Register the FFFSake forwarder engine for the given device GUID.

    Raises RuntimeError if DirectInput initialization fails.
    """

class FfbEngineType(enum.Enum):
    """Specifies the type of force feedback engine to use."""

    FORWARDER = 0
    """Direct 1:1 force feedback forwarding."""

    REDUCER_1D = 1
    """1D force reducer engine (for steering wheels)."""

    REDUCER_2D = 2
    """2D force reducer engine (for joysticks)."""

class VjoyDeviceStatus(enum.Enum):
    """Status of a virtual vJoy device."""

    kMissing = 0
    """Device is missing or driver down."""

    kFree = 1
    """Device is free and ready to acquire."""

    kBusy = 2
    """Device is owned by another application."""

    kOwned = 3
    """Device is owned by this application."""

    kUnknown = 4
    """Device status is unknown."""

class VjoyConfigInfo:
    """Configuration information and status for a vJoy device."""

    @property
    def device_id(self) -> int:
        """vJoy device ID (1-16)."""

    @property
    def status(self) -> VjoyDeviceStatus:
        """Current device status."""

    @property
    def is_full(self) -> bool:
        """
        True if the vJoy device has standard full controls (8 axes, 128 buttons, 4 hats).
        """

    @property
    def is_wheel(self) -> bool:
        """
        True if the vJoy device has steering, accelerator, and brake HID axes enabled.
        """

def GetVjoyConfigInfo(device_id: int = 1) -> VjoyConfigInfo:
    """
    Query configuration info and status for the specified vJoy device (returns VjoyConfigInfo).

    Raises:
        VjoyDriverNotEnabledError: If the vJoy driver is not enabled.
        ValueError: If device_id is outside the valid range (1-16).
    """

def GetAvailableVjoyDevices() -> list[VjoyConfigInfo]:
    """
    Enumerate all detected vJoy devices (1-16) that are configured in the driver.

    Raises:
        VjoyDriverNotEnabledError: If the vJoy driver is not enabled.
    """

class VjoyFfbController:
    """
    Controller class to forward inputs from a physical game controller to vJoy and handle force feedback.
    """

    def __init__(self) -> None: ...

    def Activate(self, device_guid: GUID, engine_type: FfbEngineType) -> bool:
        """
        Activate input forwarding and FFB engine from the physical device with the given GUID.

        Raises:
            ControllerAlreadyActiveError: If the controller is already active.
            VjoyDriverNotEnabledError: If the vJoy driver is not enabled.
            VjoyDeviceAcquireError: If acquiring the device fails.
            BackendCreationError: If backend setup fails.
            ValueError: If engine_type is invalid.
        """

    def Deactivate(self) -> None:
        """
        Deactivate input forwarding and FFB engine, releasing the acquired vJoy device.
        """

    def IsActive(self) -> bool:
        """Check if input forwarding is currently active."""

    @property
    def vjoy_device_id(self) -> int:
        """The target vJoy device ID (1-16)."""

    @vjoy_device_id.setter
    def vjoy_device_id(self, arg: int, /) -> None: ...

    def SetOptions(self, options: FffsakeOptions) -> None:
        """Set runtime options for the controller."""

    @property
    def options(self) -> FffsakeOptions:
        """Get current runtime options for the controller."""
