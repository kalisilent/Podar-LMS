import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from result.models import CourseResult
from accounts.permissions import IsLecturerOrAdmin

class StudentGradeReportPDF(APIView):
    """GET — generate PDF grade report for the current student."""
    def get(self, request):
        results = CourseResult.objects.filter(student=request.user).order_by("semester", "year")
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Podar LMS - Grade Report", styles["Title"]))
        elements.append(Paragraph(f"Student: {request.user.get_full_name()}", styles["Normal"]))
        elements.append(Spacer(1, 20))

        data = [["Course", "Semester", "Total", "Grade", "GPA", "Remark"]]
        for r in results:
            data.append([r.course.code, f"{r.semester} {r.year}",
                        f"{r.total_score:.1f}", r.grade_letter,
                        f"{r.grade_point}", r.remark])

        if len(data) > 1:
            table = Table(data, colWidths=[100, 80, 60, 50, 50, 80])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ]))
            elements.append(table)

        doc.build(elements)
        buf.seek(0)
        response = HttpResponse(buf, content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=grade_report.pdf"
        return response

class CourseAnalyticsView(APIView):
    """GET — course-level analytics for lecturers."""
    permission_classes = [IsLecturerOrAdmin]

    def get(self, request, course_id):
        from course.models import Course, Enrollment
        from assignments.models import Assignment, Submission
        from quiz.models import Quiz, QuizAttempt
        from django.db.models import Avg, Count

        course = Course.objects.get(pk=course_id)
        return Response({
            "enrolled_students": Enrollment.objects.filter(course=course, is_active=True).count(),
            "avg_assignment_grade": Submission.objects.filter(
                assignment__course=course, grade__isnull=False
            ).aggregate(avg=Avg("grade"))["avg"] or 0,
            "avg_quiz_score": QuizAttempt.objects.filter(
                quiz__course=course, completed_at__isnull=False
            ).aggregate(avg=Avg("score"))["avg"] or 0,
            "completion_rate": round(
                Enrollment.objects.filter(course=course, completed=True).count() /
                max(Enrollment.objects.filter(course=course).count(), 1) * 100, 1),
            "total_assignments": Assignment.objects.filter(course=course).count(),
            "total_quizzes": Quiz.objects.filter(course=course).count(),
        })
