import razorpay
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import get_object_or_404
from course.models import Course, Enrollment
from .models import Payment
from .serializers import PaymentSerializer, CreateOrderSerializer, VerifyPaymentSerializer

def get_razorpay_client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class CreateOrderView(APIView):
    """POST — create Razorpay order for a course."""
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = get_object_or_404(Course, pk=serializer.validated_data["course_id"])
        if course.is_free:
            return Response({"detail": "Course is free."}, status=status.HTTP_400_BAD_REQUEST)

        client = get_razorpay_client()
        order = client.order.create({
            "amount": int(course.price * 100),  # paise
            "currency": "INR",
            "payment_capture": 1,
        })
        payment = Payment.objects.create(
            user=request.user, course=course,
            amount=course.price, razorpay_order_id=order["id"])
        return Response({
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key_id": settings.RAZORPAY_KEY_ID,
            "payment_id": str(payment.id),
        })

class VerifyPaymentView(APIView):
    """POST — verify Razorpay payment and enroll student."""
    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data

        payment = get_object_or_404(Payment, razorpay_order_id=d["razorpay_order_id"])
        client = get_razorpay_client()
        try:
            client.utility.verify_payment_signature(d)
            payment.razorpay_payment_id = d["razorpay_payment_id"]
            payment.razorpay_signature = d["razorpay_signature"]
            payment.status = "completed"
            payment.save()
            Enrollment.objects.get_or_create(student=payment.user, course=payment.course)
            return Response({"detail": "Payment verified, enrolled successfully."})
        except razorpay.errors.SignatureVerificationError:
            payment.status = "failed"
            payment.save()
            return Response({"detail": "Payment verification failed."},
                          status=status.HTTP_400_BAD_REQUEST)

class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
