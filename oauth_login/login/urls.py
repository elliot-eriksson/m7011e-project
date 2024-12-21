from django.urls import path
from .views import  CustomIntrospectToken, UserList, UserDetail

# TODO behöver urls för att skapa och uppdatera användare och deleata användare
# TODO behöver urls för att skapa användarinställningar/öndra
urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('custom_introspect/', CustomIntrospectToken.as_view() , name='custom-introspect'),
   
]