class CourseRegistrationSystem:

    def __init__(self, credit_limit=24):
        self.credit_limit = credit_limit

        self.courses = {}
        self.students = {}
        self.registrations = {}

    def add_course(self, course_id, credits, capacity,
                   prerequisites=None, timetable=None):

        if credits <= 0:
            raise ValueError("Invalid course credits")

        if capacity <= 0:
            raise ValueError("Invalid course capacity")

        self.courses[course_id] = {
            "credits": credits,
            "capacity": capacity,
            "prerequisites": prerequisites or [],
            "timetable": timetable or []
        }

    def add_student(self, student_id, program, semester,
                    completed_courses=None):

        if not student_id:
            raise ValueError("Invalid student ID")

        self.students[student_id] = {
            "program": program,
            "semester": semester,
            "completed_courses": set(completed_courses or [])
        }

        self.registrations[student_id] = []

    def check_prerequisites(self, student_id, course_id):

        if student_id not in self.students:
            raise ValueError("Invalid student")

        if course_id not in self.courses:
            raise ValueError("Invalid course")

        required = self.courses[course_id]["prerequisites"]
        completed = self.students[student_id]["completed_courses"]

        return all(course in completed for course in required)

    def check_credit_limit(self, student_id, course_id):

        current_credits = self.get_total_credits(student_id)
        course_credits = self.courses[course_id]["credits"]

        return current_credits + course_credits <= self.credit_limit

    def check_timetable_clash(self, student_id, course_id):

        new_slots = set(self.courses[course_id]["timetable"])

        for registered_course in self.registrations[student_id]:
            existing_slots = set(
                self.courses[registered_course]["timetable"]
            )

            if new_slots.intersection(existing_slots):
                return True

        return False

    def check_capacity(self, course_id):

        current_count = sum(
            course_id in courses
            for courses in self.registrations.values()
        )

        return current_count < self.courses[course_id]["capacity"]

    def register_course(self, student_id, course_id):

        if student_id not in self.students:
            raise ValueError("Invalid student")

        if course_id not in self.courses:
            raise ValueError("Invalid course")

        if course_id in self.registrations[student_id]:
            raise ValueError("Duplicate registration")

        if not self.check_prerequisites(student_id, course_id):
            raise ValueError("Prerequisites not satisfied")

        if not self.check_credit_limit(student_id, course_id):
            raise ValueError("Credit limit exceeded")

        if self.check_timetable_clash(student_id, course_id):
            raise ValueError("Timetable clash")

        if not self.check_capacity(course_id):
            raise ValueError("Course capacity full")

        self.registrations[student_id].append(course_id)

        return True

    def get_total_credits(self, student_id):

        if student_id not in self.students:
            raise ValueError("Invalid student")

        return sum(
            self.courses[course_id]["credits"]
            for course_id in self.registrations[student_id]
        )


if __name__ == "__main__":

    system = CourseRegistrationSystem(credit_limit=24)

    system.add_course(
        "CS101",
        4,
        30,
        [],
        ["MON-9"]
    )

    system.add_course(
        "CS201",
        4,
        30,
        ["CS101"],
        ["TUE-10"]
    )

    system.add_course(
        "CS301",
        3,
        2,
        [],
        ["WED-11"]
    )

    system.add_student(
        "S001",
        "M.Tech Software Engineering",
        2,
        ["CS101"]
    )

    system.register_course("S001", "CS201")

    print("Registration successful")
    print("Total Registered Credits:",
          system.get_total_credits("S001"))