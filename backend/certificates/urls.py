from django.urls import path
from . import views
urlpatterns = [
    path("", views.MyCertificatesView.as_view(), name="my-certificates"),
    path("generate/<slug:course_slug>/", views.GenerateCertificateView.as_view(), name="generate-cert"),
    path("verify/<str:certificate_id>/", views.VerifyCertificateView.as_view(), name="verify-cert"),
]
