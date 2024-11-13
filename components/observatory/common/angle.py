# **************************************************************************************

# @package        @lumispace/common
# @license        Copyright © 2021-2025 Lumi.Space

# **************************************************************************************

from math import radians
from typing import TypedDict, Union

# **************************************************************************************


class Angle:
    # Decimal degrees component of the angle (0 <= dd < 360), with decimal level
    ddegrees: float

    # Decimal radians component of the angle (0 <= rad < 2 * pi):
    @property
    def radians(self) -> float:
        return radians(self.ddegrees)

    @property
    def degrees(self) -> int:
        return int(self.ddegrees)

    @property
    def minutes(self) -> int:
        return abs(int((self.ddegrees - self.degrees) * 60))

    @property
    def seconds(self) -> float:
        return (abs(self.ddegrees) - abs(self.degrees) - self.minutes / 60) * 3600

    def to_decimal_degrees(self) -> float:
        """
        Returns the azimuth angle to decimal degrees.
        """
        return self.ddegrees

    def to_radians(self) -> float:
        """
        Converts the azimuth angle to radians.
        """
        return radians(self.ddegrees)

    def to_dms(self) -> str:
        """
        Converts the azimuth angle to a degrees, minutes, and seconds (DMS) string.
        """
        return f"{self.degrees:+03d}° {self.minutes:02d}m {self.seconds:05.2f}s"


# **************************************************************************************


class AltitudinalAngleComponentsTypedDict(TypedDict):
    """
    Represents an angle in degrees, minutes, and seconds.
    """

    # Decimal degrees component of the angle (0 <= dd < 360), with decimal level
    # precision:
    ddegrees: float
    # Radians component of the angle (0 <= rad < 2 * pi):
    radians: float
    # Degrees component of the angle (0 <= deg < 360):
    degrees: int
    # Minutes component of the angle (0 <= min < 60):
    minutes: int
    # Seconds component of the angle (0 <= sec < 60), with decimal level precision:
    seconds: float


# **************************************************************************************


class AltitudinalAngle(Angle):
    """
    Represents an altitude angle, providing various standard conversion methods.

    An altitude angle is the angular distance of a celestial object above the horizon.
    It is measured vertically from the observer's horizon, ranging from -90 degrees
    (directly below the observer) to +90 degrees (directly above the observer).

    Usage:

    >>> angle = AltitudeAngle(45.0)
    """

    def __init__(self, value: Union[int, float]) -> None:
        """
        Initializes an AltitudeAngle object with the given value.
        """
        # Set the decimal degrees component of the angle:
        # Ensure the angle is normalized to the range [-90, 90]:
        self.ddegrees = self.__normalize_altitude_angle(value)

    def __normalize_altitude_angle(self, value: float) -> float:
        """
        Normalizes the given angle value to the range [-90, 90].
        """
        # Ensure the angle is normalized to the range [-90, 90]:
        ddeg = value

        if ddeg > 90:
            ddeg = 180 - ddeg

        if ddeg < -90:
            ddeg = -180 - ddeg

        return ddeg % 90 if ddeg > 0 else ddeg % -90

    def to_components(self) -> AltitudinalAngleComponentsTypedDict:
        """
        Converts the altitude angle to degrees, minutes, and seconds as well as
        decimal degrees and radians.
        """
        return {
            "ddegrees": self.ddegrees,
            "degrees": self.degrees,
            "minutes": self.minutes,
            "seconds": self.seconds,
            "radians": self.radians,
        }


# **************************************************************************************


class AzimuthalAngleComponentsTypedDict(TypedDict):
    """
    Represents an angle in degrees, minutes, and seconds.
    """

    # Decimal degrees component of the angle (0 <= dd < 360), with decimal level
    # precision:
    ddegrees: float
    # Decimal hours component of the angle (0 <= hours < 24), with decimal level
    # precision:
    dhours: float
    # Radians component of the angle (0 <= rad < 2 * pi):
    radians: float
    # Hours component of the angle (0 <= hours < 24):
    hours: float
    # Degrees component of the angle (0 <= deg < 360):
    degrees: int
    # Minutes component of the angle (0 <= min < 60):
    minutes: int
    # Seconds component of the angle (0 <= sec < 60), with decimal level precision:
    seconds: float


# **************************************************************************************


class AzimuthAngle(Angle):
    """
    Represents an azimuth angle, providing various standard conversion methods.

    An azimuth angle is a horizontal, and represents the direction of a celestial
    object from the observer's location. The angle is measured clockwise from the
    observer's north point, and is typically expressed in degrees, minutes, and
    seconds.

    The maximum value of the angle is 360 degrees, and the minimum value is 0.

    Usage:

    >>> angle = AzimuthAngle(45.0)
    """

    # Decimal hours component of the angle (0 <= hours < 24):
    @property
    def dhours(self) -> float:
        return self.ddegrees / 15

    @property
    def hours(self) -> int:
        # Here we take the degree component of the hour angle:
        return int(self.degrees / 15)

    def __init__(self, value: Union[int, float]) -> None:
        """
        Initializes an AzimuthAngle object with the given value.
        """
        # Set the decimal degrees component of the angle:
        # Ensure the angle is normalized to the range [0, 360):
        # N.B. All other properties are derived from this value:
        self.ddegrees = self.__normalize_azimuthal_angle(value)

    def __normalize_azimuthal_angle(self, value: float) -> float:
        """
        Normalizes the given angle value to the range [0, 360).
        """
        # Ensure the angle is normalized to the range [-360, 360):
        ddeg = value % 360.0

        # Ensure the angle is positive, in the range [0, 360):
        if ddeg < 0:
            ddeg += 360.0

        return ddeg

    def to_decimal_hours(self) -> float:
        """
        Returns the azimuth angle to decimal hours.
        """
        return self.dhours

    def to_hms(self) -> str:
        """
        Converts the azimuth angle to a hours, minutes, and seconds (HMS) string.
        """
        return f"{self.hours:02d}h {self.minutes:02d}m {self.seconds:05.2f}s"

    def to_components(self) -> AzimuthalAngleComponentsTypedDict:
        """
        Converts the azimuth angle to degrees, minutes, and seconds as well
        as decimal degrees, decimal hours, and radians.
        """
        return {
            "hours": self.hours,
            "ddegrees": self.ddegrees,
            "dhours": self.dhours,
            "degrees": self.degrees,
            "minutes": self.minutes,
            "seconds": self.seconds,
            "radians": self.radians,
        }


# **************************************************************************************
