from django.urls import path
from .views import  *

# TODO behöver urls för att skapa och uppdatera användare och deleata användare
# TODO behöver urls för att skapa användarinställningar/öndra
urlpatterns = [
    path('delete_user/', UserDeleteView.as_view(), name='delete_user'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('update_password/', PasswordUpdateView.as_view(), name='update_password'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('custom_introspect/', CustomIntrospectToken.as_view() , name='custom-introspect'),
   
]