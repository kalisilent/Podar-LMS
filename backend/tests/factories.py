import factory
from django.contrib.auth import get_user_model
from course.models import Program, Course, Section, Lesson

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    username = factory.Sequence(lambda n: f"user{n}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = "student"
    password = factory.PostGenerationMethodCall("set_password", "testpass123")


class LecturerFactory(UserFactory):
    role = "lecturer"
    email = factory.Sequence(lambda n: f"lecturer{n}@test.com")
    username = factory.Sequence(lambda n: f"lecturer{n}")


class AdminFactory(UserFactory):
    role = "admin"
    is_staff = True
    email = factory.Sequence(lambda n: f"admin{n}@test.com")
    username = factory.Sequence(lambda n: f"admin{n}")


class ProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Program

    title = factory.Sequence(lambda n: f"Program {n}")


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.Sequence(lambda n: f"Course {n}")
    slug = factory.Sequence(lambda n: f"course-{n}")
    code = factory.Sequence(lambda n: f"CS{100 + n}")
    description = "Test course description"
    lecturer = factory.SubFactory(LecturerFactory)
    is_published = True
    is_free = True


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Section

    course = factory.SubFactory(CourseFactory)
    title = factory.Sequence(lambda n: f"Section {n}")
    order = factory.Sequence(lambda n: n)


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lesson

    section = factory.SubFactory(SectionFactory)
    title = factory.Sequence(lambda n: f"Lesson {n}")
    lesson_type = "text"
    content = "Sample content"
    order = factory.Sequence(lambda n: n)
