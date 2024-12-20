from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailLogViewSet

router = DefaultRouter()
router.register(r'email_logs', EmailLogViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]
