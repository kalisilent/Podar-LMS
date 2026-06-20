from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    # API v1
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/courses/", include("course.urls")),
    path("api/v1/assignments/", include("assignments.urls")),
    path("api/v1/quizzes/", include("quiz.urls")),
    path("api/v1/forums/", include("forums.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
    path("api/v1/certificates/", include("certificates.urls")),
    path("api/v1/payments/", include("payments.urls")),
    path("api/v1/results/", include("result.urls")),
    path("api/v1/reports/", include("reports.urls")),
    # Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    # Health
    path("health/", lambda r: __import__("django.http", fromlist=["JsonResponse"]).JsonResponse({"status": "ok"})),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
