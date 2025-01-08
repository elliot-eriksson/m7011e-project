from django.urls import path
from .views import EmailLogView

urlpatterns = [
    path('emails/', EmailLogView.as_view({'get': 'list', 'post': 'create'})),
]
