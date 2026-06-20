"""
Seed the database with sample data for development.
Usage: python manage.py seed
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with sample users, courses, assignments, quizzes"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # ── Users ──
        admin = self._create_user("admin@podar-lms.io", "Admin", "User", "admin", "admin123")
        lec1 = self._create_user("lecturer1@podar-lms.io", "Rahul", "Sharma", "lecturer", "lecturer123")
        lec2 = self._create_user("lecturer2@podar-lms.io", "Priya", "Patel", "lecturer", "lecturer123")
        stu1 = self._create_user("student1@podar-lms.io", "Arjun", "Mehta", "student", "student123")
        stu2 = self._create_user("student2@podar-lms.io", "Ananya", "Singh", "student", "student123")
        stu3 = self._create_user("student3@podar-lms.io", "Rohan", "Kumar", "student", "student123")

        # ── Programs ──
        from course.models import Program, Course, Section, Lesson, Enrollment
        prog, _ = Program.objects.get_or_create(title="B.Tech Computer Science", defaults={"description": "Undergraduate CS program"})

        # ── Courses ──
        courses_data = [
            {"title": "Design and Analysis of Algorithms", "code": "CS301", "lecturer": lec1, "level": "intermediate", "description": "Covers sorting, searching, graph algorithms, dynamic programming, and NP-completeness."},
            {"title": "Web Development Fundamentals", "code": "CS201", "lecturer": lec1, "level": "beginner", "description": "HTML, CSS, JavaScript, React basics, and building modern web apps.", "is_free": True},
            {"title": "Machine Learning", "code": "CS401", "lecturer": lec2, "level": "advanced", "description": "Supervised and unsupervised learning, neural networks, and practical ML projects.", "price": 2999},
            {"title": "Database Management Systems", "code": "CS302", "lecturer": lec2, "level": "intermediate", "description": "Relational databases, SQL, normalization, transactions, and indexing."},
            {"title": "Operating Systems", "code": "CS303", "lecturer": lec1, "level": "intermediate", "description": "Processes, threads, memory management, file systems, and concurrency."},
        ]

        courses = []
        for cd in courses_data:
            course, _ = Course.objects.get_or_create(
                code=cd["code"],
                defaults={**cd, "slug": slugify(cd["title"]), "program": prog, "is_published": True,
                          "is_free": cd.get("is_free", True), "price": cd.get("price", 0),
                          "semester": "Monsoon", "year": 2025}
            )
            courses.append(course)

        # ── Sections & Lessons ──
        for course in courses:
            if course.sections.exists():
                continue
            for i in range(1, 4):
                section = Section.objects.create(course=course, title=f"Module {i}", order=i,
                                                  description=f"Week {i} content for {course.code}")
                for j in range(1, 4):
                    lt = ["video", "pdf", "text"][j - 1]
                    Lesson.objects.create(
                        section=section, title=f"Lesson {i}.{j} — {lt.upper()} content",
                        lesson_type=lt, order=j, duration_minutes=15 + j * 5,
                        content=f"Sample content for lesson {i}.{j}" if lt == "text" else "",
                        is_preview=(i == 1 and j == 1),
                    )

        # ── Enrollments ──
        for stu in [stu1, stu2, stu3]:
            for course in courses[:3]:
                Enrollment.objects.get_or_create(student=stu, course=course)

        # ── Assignments ──
        from assignments.models import Assignment
        now = timezone.now()
        for course in courses[:3]:
            for i in range(1, 3):
                Assignment.objects.get_or_create(
                    course=course, title=f"{course.code} Assignment {i}",
                    defaults={
                        "description": f"Complete the following problems for {course.title}.",
                        "total_marks": 100, "due_date": now + timedelta(days=7 * i),
                        "is_published": True, "created_by": course.lecturer,
                    }
                )

        # ── Quizzes ──
        from quiz.models import Quiz, Question, Choice
        for course in courses[:2]:
            quiz, created = Quiz.objects.get_or_create(
                course=course, title=f"{course.code} Mid-semester Quiz",
                defaults={
                    "time_limit_minutes": 30, "max_attempts": 2,
                    "pass_percentage": 50, "is_published": True,
                    "created_by": course.lecturer,
                }
            )
            if created:
                for qi in range(1, 6):
                    q = Question.objects.create(
                        quiz=quiz, text=f"Sample question {qi} for {course.code}?",
                        question_type="mcq", marks=2, order=qi,
                        explanation=f"The correct answer is option A.",
                    )
                    for ci, (text, correct) in enumerate([
                        ("Option A (correct)", True), ("Option B", False),
                        ("Option C", False), ("Option D", False),
                    ]):
                        Choice.objects.create(question=q, text=text, is_correct=correct)

        # ── Forums ──
        from forums.models import Forum, Thread
        for course in courses[:3]:
            forum, _ = Forum.objects.get_or_create(course=course)
            Thread.objects.get_or_create(
                forum=forum, title=f"Welcome to {course.code} discussions",
                defaults={"author": course.lecturer, "content": "Feel free to ask questions here!", "is_pinned": True}
            )

        # ── Grade Scale ──
        from result.models import GradeScale
        grades = [
            ("A+", 90, 100, 10, "Outstanding"), ("A", 80, 89.99, 9, "Excellent"),
            ("B+", 70, 79.99, 8, "Very Good"), ("B", 60, 69.99, 7, "Good"),
            ("C+", 50, 59.99, 6, "Above Average"), ("C", 40, 49.99, 5, "Average"),
            ("D", 30, 39.99, 4, "Below Average"), ("F", 0, 29.99, 0, "Fail"),
        ]
        for letter, mn, mx, gp, remark in grades:
            GradeScale.objects.get_or_create(
                letter=letter, defaults={"min_percentage": mn, "max_percentage": mx,
                                         "grade_point": gp, "remark": remark}
            )

        self.stdout.write(self.style.SUCCESS(
            f"Done! Created {User.objects.count()} users, {Course.objects.count()} courses, "
            f"{Assignment.objects.count()} assignments, {Quiz.objects.count()} quizzes."
        ))
        self.stdout.write(self.style.WARNING(
            "\nLogin credentials:\n"
            "  Admin:    admin@podar-lms.io / admin123\n"
            "  Lecturer: lecturer1@podar-lms.io / lecturer123\n"
            "  Student:  student1@podar-lms.io / student123"
        ))

    def _create_user(self, email, first, last, role, password):
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0], "first_name": first,
                       "last_name": last, "role": role, "is_verified": True}
        )
        if created:
            user.set_password(password)
            if role == "admin":
                user.is_staff = True
                user.is_superuser = True
            user.save()
            # Create profiles
            if role == "student":
                from accounts.models import StudentProfile
                StudentProfile.objects.get_or_create(user=user)
            elif role == "lecturer":
                from accounts.models import LecturerProfile
                LecturerProfile.objects.get_or_create(user=user)
        return user
