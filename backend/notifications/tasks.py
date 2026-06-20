from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email_notification(recipient_email, subject, message):
    """Send an email notification asynchronously."""
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER or "noreply@podar-lms.io",
        recipient_list=[recipient_email],
        fail_silently=True,
    )


@shared_task
def send_assignment_reminder():
    """Periodic task: remind students of upcoming due assignments."""
    from django.utils import timezone
    from datetime import timedelta
    from assignments.models import Assignment
    from course.models import Enrollment
    from notifications.utils import send_notification

    tomorrow = timezone.now() + timedelta(days=1)
    upcoming = Assignment.objects.filter(
        due_date__date=tomorrow.date(), is_published=True
    )

    for assignment in upcoming:
        enrolled_students = Enrollment.objects.filter(
            course=assignment.course, is_active=True
        ).select_related("student")

        for enrollment in enrolled_students:
            # Skip if already submitted
            if assignment.submissions.filter(student=enrollment.student).exists():
                continue

            send_notification(
                recipient=enrollment.student,
                title=f"Assignment due tomorrow: {assignment.title}",
                message=f"Your assignment '{assignment.title}' for {assignment.course.code} is due tomorrow.",
                notif_type="assignment",
                link=f"/assignments",
            )


@shared_task
def send_grade_notification(student_id, assignment_title, grade):
    """Notify a student that their assignment has been graded."""
    from django.contrib.auth import get_user_model
    from notifications.utils import send_notification

    User = get_user_model()
    try:
        student = User.objects.get(pk=student_id)
        send_notification(
            recipient=student,
            title=f"Grade posted: {assignment_title}",
            message=f"You received {grade} on '{assignment_title}'.",
            notif_type="grade",
            link="/grades",
        )
    except User.DoesNotExist:
        pass


@shared_task
def generate_certificate_async(certificate_id):
    """Generate certificate PDF in background."""
    from certificates.models import Certificate
    from certificates.utils import generate_certificate_pdf

    try:
        cert = Certificate.objects.get(pk=certificate_id)
        if not cert.pdf_file:
            generate_certificate_pdf(cert)
    except Certificate.DoesNotExist:
        pass
