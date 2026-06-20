import io
import qrcode
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.conf import settings
from django.core.files.base import ContentFile

def generate_certificate_pdf(certificate):
    """Generate a PDF certificate with QR code."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=landscape(A4))
    w, h = landscape(A4)

    # Border
    c.setStrokeColor(colors.HexColor("#1e40af"))
    c.setLineWidth(3)
    c.rect(30, 30, w - 60, h - 60)

    # Title
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(colors.HexColor("#1e3a5f"))
    c.drawCentredString(w / 2, h - 120, "Certificate of Completion")

    # Line
    c.setStrokeColor(colors.HexColor("#3b82f6"))
    c.setLineWidth(1)
    c.line(200, h - 140, w - 200, h - 140)

    # Student name
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(colors.black)
    c.drawCentredString(w / 2, h - 200, certificate.student.get_full_name())

    # Course
    c.setFont("Helvetica", 18)
    c.drawCentredString(w / 2, h - 250, "has successfully completed")
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(w / 2, h - 290, certificate.course.title)

    # Date
    c.setFont("Helvetica", 14)
    c.drawCentredString(w / 2, h - 340, f"Issued on: {certificate.issued_at.strftime('%B %d, %Y')}")

    # Certificate ID
    c.setFont("Helvetica", 11)
    c.drawCentredString(w / 2, h - 370, f"Certificate ID: {certificate.certificate_id}")

    # QR Code
    verify_url = f"{settings.FRONTEND_URL}/verify/{certificate.certificate_id}"
    qr_img = qrcode.make(verify_url)
    qr_buf = io.BytesIO()
    qr_img.save(qr_buf, format="PNG")
    qr_buf.seek(0)
    from reportlab.lib.utils import ImageReader
    c.drawImage(ImageReader(qr_buf), w - 160, 50, 100, 100)

    c.save()
    buf.seek(0)
    certificate.pdf_file.save(f"{certificate.certificate_id}.pdf", ContentFile(buf.read()), save=True)
    return certificate
