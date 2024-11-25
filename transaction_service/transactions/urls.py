from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet


router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    # path ('', include(router.urls)),
    path('transactions/', TransactionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('transactions/<int:pk>/', TransactionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('transactions/by-budget/<int:pk>/', TransactionViewSet.as_view({
        'get': 'listByBudget'
    })),
    path('transactions/by-user/', TransactionViewSet.as_view({
        'get': 'listByUser'
    })),
]