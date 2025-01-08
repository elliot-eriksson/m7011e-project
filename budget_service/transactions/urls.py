from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet


transaction_detail = TransactionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
        'post': 'create'
    })
transaction_by_budget = TransactionViewSet.as_view({
        'get': 'listByBudget'
    })
transaction_by_user = TransactionViewSet.as_view({
        'get': 'listByUser'
    })
urlpatterns = [
    path('transactions/<slug:slug>/',transaction_detail, name='transaction-detail'),
    path('transactions/by-budget/<slug:slug>/', transaction_by_budget, name='transaction-by-budget'),
    path('transactions/by-user/<str:username>/', transaction_by_user, name='transaction-by-user'),
]