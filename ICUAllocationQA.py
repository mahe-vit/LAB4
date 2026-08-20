import unittest
from ICUAllocation import ICUAllocationSystem


class ICUAllocationQA(unittest.TestCase):

    # 1. Critical patient
    def test_critical_patient(self):

        icu = ICUAllocationSystem(2)

        patient = icu.admit_patient(
            "P001",
            65,
            85,
            130,
            "90/60",
            39.5
        )

        self.assertEqual(
            patient["priority"],
            "CRITICAL"
        )

    # 2. Normal patient
    def test_normal_patient(self):

        icu = ICUAllocationSystem(2)

        patient = icu.admit_patient(
            "P002",
            30,
            98,
            75,
            "120/80",
            36.8
        )

        self.assertEqual(
            patient["priority"],
            "LOW"
        )

        self.assertEqual(
            patient["status"],
            "ICU ALLOCATED"
        )

    # 3. Emergency case
    def test_emergency_case(self):

        icu = ICUAllocationSystem(1)

        patient = icu.admit_patient(
            "P003",
            45,
            98,
            80,
            "120/80",
            37.0,
            emergency=True
        )

        self.assertEqual(
            patient["priority"],
            "CRITICAL"
        )

    # 4. No ICU beds
    def test_no_icu_beds(self):

        icu = ICUAllocationSystem(0)

        patient = icu.admit_patient(
            "P004",
            60,
            90,
            110,
            "100/70",
            38.5
        )

        self.assertEqual(
            patient["status"],
            "WAITING LIST"
        )

        self.assertEqual(
            len(icu.waiting_list),
            1
        )

    # 5. Duplicate patient
    def test_duplicate_patient(self):

        icu = ICUAllocationSystem(2)

        icu.admit_patient(
            "P005",
            50,
            95,
            80,
            "120/80",
            37.0
        )

        with self.assertRaises(ValueError):
            icu.admit_patient(
                "P005",
                55,
                90,
                100,
                "110/70",
                38.0
            )

    # 6. Invalid oxygen level
    def test_invalid_oxygen_level(self):

        icu = ICUAllocationSystem(2)

        with self.assertRaises(ValueError):
            icu.admit_patient(
                "P006",
                40,
                150,
                80,
                "120/80",
                37.0
            )

    # 7. Invalid heart rate
    def test_invalid_heart_rate(self):

        icu = ICUAllocationSystem(2)

        with self.assertRaises(ValueError):
            icu.admit_patient(
                "P007",
                40,
                98,
                0,
                "120/80",
                37.0
            )

    # 8. Priority boundary values
    def test_priority_boundary_values(self):

        icu = ICUAllocationSystem(3)

        patient = icu.admit_patient(
            "P008",
            50,
            94,
            101,
            "120/80",
            38.0
        )

        self.assertIn(
            patient["priority"],
            ["MEDIUM", "HIGH", "CRITICAL"]
        )

    # 9. Multiple patients competing for same bed
    def test_multiple_patients_same_bed(self):

        icu = ICUAllocationSystem(1)

        first = icu.admit_patient(
            "P009",
            60,
            98,
            75,
            "120/80",
            37.0
        )

        second = icu.admit_patient(
            "P010",
            70,
            82,
            130,
            "90/60",
            39.5
        )

        self.assertEqual(
            first["status"],
            "ICU ALLOCATED"
        )

        self.assertEqual(
            second["status"],
            "WAITING LIST"
        )

        self.assertEqual(
            len(icu.waiting_list),
            1
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)