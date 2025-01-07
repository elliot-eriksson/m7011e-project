from django.urls import path

# from rest_framework.routers import DefaultRouter
from .views import EmailLogView

# router = DefaultRouter()
# router.register(r'email_logs', EmailLogViewSet)

# TODO: lägg till CRUD endpoints för email_logs
urlpatterns = [
    path('emails/', EmailLogView.as_view({'get': 'list', 'post': 'create'})),
]
