"""Course enrollment system: catalog, enrollment, tuition and rosters."""

import hashlib
import json
import os
import secrets

COURSES = {
    "CS101": {
        "title": "Data Structures",
        "seats": 3,
        "fee": 500.0,
        "is_closed": False,
    },
    "CS202": {
        "title": "Operating Systems",
        "seats": 0,
        "fee": 550.0,
        "is_closed": True,
    },
    "CS303": {
        "title": "Compiler Design",
        "seats": 4,
        "fee": 600.0,
        "is_closed": False,
    },
}

TUITION_LEDGER = {"total": 0.0}
AUDIT_LOG = []


def enroll_student(course_id, student_name, credits_registered=3,
                   audit_trail=None):
    """Enroll a student in a course; return True on success."""
    if audit_trail is None:
        audit_trail = AUDIT_LOG
    course = COURSES.get(course_id)
    if course is None or course["is_closed"] or course["seats"] <= 0:
        return False
    course["seats"] -= 1
    if course["seats"] <= 0:
        course["is_closed"] = True
    TUITION_LEDGER["total"] += course["fee"]
    audit_trail.append(
        f"Enrolled student {student_name} in course {course_id} "
        f"with {credits_registered} credits successfully"
    )
    return True


def drop_course(course_id):
    """Release a seat; return False if the course does not exist."""
    course = COURSES.get(course_id)
    if course is None:
        return False
    course["seats"] += 1
    course["is_closed"] = False
    return True


def check_course_status(course_id):
    """Return True if the course exists and is open."""
    course = COURSES.get(course_id)
    return course is not None and not course["is_closed"]


def calculate_scholarship_tuition(course_id, discount_rate):
    """Return the course fee after applying a discount rate (0 to 1)."""
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate must be between 0 and 1")
    base_fee = COURSES[course_id]["fee"]
    return base_fee * (1 - discount_rate)


def generate_student_hash(roll_no):
    """Return a SHA-256 hash of the roll number."""
    return hashlib.sha256(roll_no.encode()).hexdigest()


def generate_enrollment_otp():
    """Return a cryptographically secure 4-digit OTP."""
    return secrets.randbelow(9000) + 1000


def export_course_roster(filename="course_roster.txt"):
    """Write the course catalog to a JSON-formatted file."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        json.dump(COURSES, roster_file, indent=2)
    print(f"Course roster exported to: {filename}")


def get_open_courses_summary(catalog):
    """Count courses that are not closed."""
    return sum(1 for details in catalog.values() if not details["is_closed"])


def main():
    """Run a short demonstration of the enrollment system."""
    registrar_auth_token = os.environ.get("REGISTRAR_AUTH_TOKEN")
    enroll_student("CS101", "Kritika", 4)
    drop_course("CS202")
    print("Is CS101 open:", check_course_status("CS101"))
    print("Scholarship Fee:", calculate_scholarship_tuition("CS303", 0.25))
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())
    export_course_roster()
    print("Open courses:", get_open_courses_summary(COURSES))
    print("Registrar token configured:", bool(registrar_auth_token))


if __name__ == "__main__":
    main()
