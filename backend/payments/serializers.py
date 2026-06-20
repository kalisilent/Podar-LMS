from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["user", "status", "razorpay_order_id"]

class CreateOrderSerializer(serializers.Serializer):
    course_id = serializers.UUIDField()

class VerifyPaymentSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField()
    razorpay_payment_id = serializers.CharField()
    razorpay_signature = serializers.CharField()
