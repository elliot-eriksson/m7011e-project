from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet

transaction_list = TransactionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })

transaction_detail = TransactionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })
transaction_by_budget = TransactionViewSet.as_view({
        'get': 'listByBudget'
    })
transaction_by_user = TransactionViewSet.as_view({
        'get': 'listByUser'
    })
urlpatterns = [
    # path ('', include(router.urls)),
    path('transactions/',transaction_list, name='transaction-list'),
    path('transactions/<slug:slug>/',transaction_detail, name='transaction-detail'),
    path('transactions/by-budget/<slug:slug>/', transaction_by_budget, name='transaction-by-budget'),
    path('transactions/by-user/<slug:slug>/', transaction_by_user, name='transaction-by-user'),
]