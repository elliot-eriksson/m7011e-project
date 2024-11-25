from django.urls import path

from .views import *

budget_list = BudgetViewSet.as_view({'get': 'list', 'post': 'create'})
budget_detail = BudgetViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

# BudgetAccessViewSet URLs
budget_access_list = BudgetAccessViewSet.as_view({'get': 'list', 'post': 'create'})
budget_access_detail = BudgetAccessViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
budget_access_by_user = BudgetAccessViewSet.as_view({'get': 'listBudgetAccessByUser'})
budget_access_by_budget = BudgetAccessViewSet.as_view({'get': 'listBudgetAccessByBudget'})

urlpatterns = [
    path('budgets/', budget_list, name='budget-list'),
    path('budgets/<int:pk>/', budget_detail, name='budget-detail'),

    path('budget-access/', budget_access_list, name='budget-access-list'),
    path('budget-access/<int:pk>/', budget_access_detail, name='budget-access-detail'),
    path('budget-access/user/<int:user_id>/', budget_access_by_user, name='budget-access-by-user'),
    path('budget-access/budget/<int:budget_id>/', budget_access_by_budget, name='budget-access-by-budget'),

    # path('user/', UserAPIView.as_view(), name='user-list'),

]

