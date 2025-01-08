from django.urls import path
from .views import  *


urlpatterns = [
    path('delete_user/<str:username>/', UserDeleteView.as_view(), name='delete_user'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('update_password/', PasswordUpdateView.as_view(), name='update_password'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('g2fa/<str:action>/', G2FAView.as_view(), name='g2fa_action'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
]