import unittest
from CourseRegistration import CourseRegistrationSystem


class CourseRegistrationQA(unittest.TestCase):

    def setUp(self):

        self.system = CourseRegistrationSystem(
            credit_limit=8
        )

        # Course 1
        self.system.add_course(
            "CS101",
            4,
            30,
            [],
            ["MON-9"]
        )

        # Course 2 - requires CS101
        self.system.add_course(
            "CS201",
            4,
            30,
            ["CS101"],
            ["TUE-10"]
        )

        # Course 3 - 3 credits, capacity 2
        self.system.add_course(
            "CS301",
            3,
            2,
            [],
            ["WED-11"]
        )

        # Course 4 - clashes with CS101
        self.system.add_course(
            "CS401",
            4,
            30,
            [],
            ["MON-9"]
        )

        # Course 5 - 5 credits, exceeds remaining credit limit
        self.system.add_course(
            "CS501",
            5,
            30,
            [],
            ["THU-10"]
        )

        # Student
        self.system.add_student(
            "S001",
            "M.Tech",
            2,
            ["CS101"]
        )

    # 1. Prerequisite verification
    def test_prerequisite(self):

        self.system.register_course(
            "S001",
            "CS201"
        )

        self.assertIn(
            "CS201",
            self.system.registrations["S001"]
        )

    # 2. Credit limit
    def test_credit_limit(self):

        # 4 credits already registered
        self.system.register_course(
            "S001",
            "CS201"
        )

        # 4 + 5 = 9, which exceeds limit of 8
        with self.assertRaises(ValueError):
            self.system.register_course(
                "S001",
                "CS501"
            )

    # 3. Timetable clash
    def test_timetable_clash(self):

        self.system.register_course(
            "S001",
            "CS101"
        )

        with self.assertRaises(ValueError):
            self.system.register_course(
                "S001",
                "CS401"
            )

    # 4. Course capacity
    def test_course_capacity(self):

        self.system.add_student(
            "S002",
            "M.Tech",
            2,
            []
        )

        self.system.add_student(
            "S003",
            "M.Tech",
            2,
            []
        )

        self.system.register_course(
            "S002",
            "CS301"
        )

        self.system.register_course(
            "S003",
            "CS301"
        )

        self.system.add_student(
            "S004",
            "M.Tech",
            2,
            []
        )

        with self.assertRaises(ValueError):
            self.system.register_course(
                "S004",
                "CS301"
            )

    # 5. Duplicate registration
    def test_duplicate_registration(self):

        self.system.register_course(
            "S001",
            "CS201"
        )

        with self.assertRaises(ValueError):
            self.system.register_course(
                "S001",
                "CS201"
            )

    # 6. Total registered credits
    def test_total_credits(self):

        self.system.register_course(
            "S001",
            "CS201"
        )

        self.assertEqual(
            self.system.get_total_credits("S001"),
            4
        )

    # 7. Invalid student
    def test_invalid_student(self):

        with self.assertRaises(ValueError):
            self.system.register_course(
                "INVALID",
                "CS201"
            )

    # 8. Invalid course
    def test_invalid_course(self):

        with self.assertRaises(ValueError):
            self.system.register_course(
                "S001",
                "INVALID"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)