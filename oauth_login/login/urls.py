from django.urls import path
from .views import  CustomIntrospectToken, UserList, UserDetail, ValidateTokenView

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('validate_token/', ValidateTokenView.as_view() , name='validate-token'),
    # path('introspect/', CustomTokenIntrospectionView.as_view(), name="token_introspection"),
    path('custom_introspect/', CustomIntrospectToken.as_view() , name='custom-introspect'),

    
]