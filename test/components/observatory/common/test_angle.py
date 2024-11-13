# **************************************************************************************

# @package        @lumispace/common
# @license        Copyright © 2021-2025 Lumi.Space

# **************************************************************************************

import unittest

from observatory.common.angle import (
    AltitudinalAngle,
    AltitudinalAngleComponentsTypedDict,
    AzimuthalAngleComponentsTypedDict,
    AzimuthAngle,
)

# **************************************************************************************


class TestAltitudinalAngle(unittest.TestCase):
    def test_angle_int_value(self) -> None:
        angle: AltitudinalAngle = AltitudinalAngle(45)
        self.assertEqual(angle.ddegrees, 45)
        self.assertEqual(angle.degrees, 45)
        self.assertEqual(angle.minutes, 0)
        self.assertEqual(angle.seconds, 0)

    def test_angle_float_value(self) -> None:
        angle: AltitudinalAngle = AltitudinalAngle(45.8)
        self.assertEqual(angle.ddegrees, 45.8)
        self.assertEqual(angle.degrees, 45)
        self.assertEqual(angle.minutes, 47)
        self.assertAlmostEqual(angle.seconds, 59.99, 1)

    def test_angle_properties(self) -> None:
        angle: AltitudinalAngle = AltitudinalAngle(45.8)
        self.assertEqual(angle.ddegrees, 45.8)
        self.assertEqual(angle.degrees, 45)
        self.assertEqual(angle.minutes, 47)
        self.assertAlmostEqual(angle.seconds, 59.99, 1)

    def test_angle_normalization_positive(self) -> None:
        angle: AltitudinalAngle = AltitudinalAngle(91)
        self.assertEqual(angle.ddegrees, 89)
        self.assertEqual(angle.degrees, 89)
        self.assertEqual(angle.minutes, 0)
        self.assertEqual(angle.seconds, 0)

    def test_angle_normalization_negative(self) -> None:
        angle: AltitudinalAngle = AltitudinalAngle(-45)
        self.assertEqual(angle.ddegrees, -45)
        self.assertEqual(angle.degrees, -45)
        self.assertEqual(angle.minutes, 0)
        self.assertEqual(angle.seconds, 0)

    def test_angle_to_decimal_degrees(self) -> None:
        angle: float = AltitudinalAngle(30.1506).to_decimal_degrees()
        self.assertEqual(angle, 30.1506)

    def test_angle_to_radians(self) -> None:
        angle: float = AltitudinalAngle(30.1506).to_radians()
        self.assertEqual(angle, 0.5262272414518023)

    def test_angle_to_components(self) -> None:
        angle: AltitudinalAngleComponentsTypedDict = AltitudinalAngle(
            45
        ).to_components()

        self.assertEqual(angle["ddegrees"], 45)
        self.assertEqual(angle["degrees"], 45)
        self.assertEqual(angle["minutes"], 0)
        self.assertEqual(angle["seconds"], 0)

    def test_angle_to_dms_positive(self) -> None:
        angle = AltitudinalAngle(45.8)
        dms = angle.to_dms()
        self.assertEqual(dms, "+45° 47m 60.00s")

    def test_angle_to_dms_negative(self) -> None:
        angle = AltitudinalAngle(-45.8)
        dms = angle.to_dms()
        self.assertEqual(dms, "-45° 47m 60.00s")


# **************************************************************************************


class TestAzimuthAngle(unittest.TestCase):
    def test_angle_int_value(self) -> None:
        angle: AzimuthAngle = AzimuthAngle(45)
        self.assertEqual(angle.ddegrees, 45)
        self.assertEqual(angle.hours, 3)
        self.assertEqual(angle.dhours, 3.0)
        self.assertAlmostEqual(angle.degrees, 45)
        self.assertEqual(angle.minutes, 0)
        self.assertEqual(angle.seconds, 0)

    def test_angle_float_value(self) -> None:
        angle: AzimuthAngle = AzimuthAngle(45.8)
        self.assertEqual(angle.ddegrees, 45.8)
        self.assertAlmostEqual(angle.hours, 3.0, 2)
        self.assertAlmostEqual(angle.dhours, 3.0533, 2)
        self.assertAlmostEqual(angle.degrees, 45)
        self.assertEqual(angle.minutes, 47)
        self.assertAlmostEqual(angle.seconds, 59.99, 1)

    def test_angle_properties(self) -> None:
        angle: AzimuthAngle = AzimuthAngle(45.8)
        self.assertEqual(angle.ddegrees, 45.8)
        self.assertAlmostEqual(angle.hours, 3.0, 2)
        self.assertAlmostEqual(angle.dhours, 3.0533, 2)
        self.assertEqual(angle.degrees, 45)
        self.assertEqual(angle.minutes, 47)
        self.assertAlmostEqual(angle.seconds, 59.99, 1)

    def test_angle_normalization_positive(self) -> None:
        angle: AzimuthAngle = AzimuthAngle(405)
        self.assertEqual(angle.ddegrees, 45)
        self.assertEqual(angle.hours, 3)
        self.assertAlmostEqual(angle.dhours, 3.0, 2)
        self.assertEqual(angle.degrees, 45)
        self.assertEqual(angle.minutes, 0)
        self.assertEqual(angle.seconds, 0)

    def test_angle_normalization_negative(self) -> None:
        angle: AzimuthAngle = AzimuthAngle(-45)
        self.assertEqual(angle.ddegrees, 315)
        self.assertEqual(angle.hours, 21)
        self.assertAlmostEqual(angle.dhours, 21, 2)
        self.assertEqual(angle.degrees, 315)
        self.assertEqual(angle.minutes, 0)
        self.assertEqual(angle.seconds, 0)

    def test_angle_to_decimal_degrees(self) -> None:
        angle: float = AzimuthAngle(30.1506).to_decimal_degrees()
        self.assertEqual(angle, 30.1506)

    def test_angle_to_radians(self) -> None:
        angle: float = AzimuthAngle(30.1506).to_radians()
        self.assertEqual(angle, 0.5262272414518023)

    def test_angle_to_components(self) -> None:
        angle: AzimuthalAngleComponentsTypedDict = AzimuthAngle(45).to_components()

        self.assertEqual(angle["ddegrees"], 45)
        self.assertEqual(angle["hours"], 3)
        self.assertEqual(angle["degrees"], 45)
        self.assertEqual(angle["minutes"], 0)
        self.assertEqual(angle["seconds"], 0)

    def test_angle_to_dms_positive(self) -> None:
        angle = AzimuthAngle(45.8)
        dms = angle.to_dms()
        self.assertEqual(dms, "+45° 47m 60.00s")

    def test_angle_to_dms_negative(self) -> None:
        angle = AzimuthAngle(-45.8)
        dms = angle.to_dms()
        self.assertEqual(dms, "+314° 11m 60.00s")

    def test_angle_to_hms_positive(self) -> None:
        angle = AzimuthAngle(45.8)
        dms = angle.to_hms()
        self.assertEqual(dms, "03h 47m 60.00s")

    def test_angle_to_hms_negative(self) -> None:
        angle = AzimuthAngle(-45.8)
        hms = angle.to_hms()
        self.assertEqual(hms, "20h 11m 60.00s")


# **************************************************************************************
