from django.urls import path

from .views import *

budget_list = BudgetViewSet.as_view({'get': 'list', 'post': 'create'})
budget_detail = BudgetViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

# BudgetAccessViewSet URLs
# budget_access_list = BudgetAccessViewSet.as_view({})
budget_access_detail = BudgetAccessViewSet.as_view({'get': 'retrieve', 'put': 'update'})
budget_access_delete = BudgetAccessViewSet.as_view({'delete': 'deleteBudgetAccess'})

budget_access_by_user = BudgetAccessViewSet.as_view({'get': 'listBudgetAccessByUser'})
budget_access_by_budget = BudgetAccessViewSet.as_view({'get': 'listBudgetAccessByBudget'})

budget_accept_invitation = BudgetInvitationAcceptViewSet.as_view({'get': 'accept_invitation', 'post': 'addBudgetAccess'})

urlpatterns = [
    # UnitTest exists
    path('budgets/', budget_list, name='budget-list'),
    path('budgets/<int:pk>/', budget_detail, name='budget-detail'),

    # No UnitTest
    path('invitations/accept/<str:token>', budget_accept_invitation, name='budget_accept_invitation'),
    # UnitTest exists not done yet
    path('budget-access/<int:pk>/', budget_access_detail, name='budget-access-detail'),
    path('budget-access/delete/<int:budgetID>/<str:username>/', budget_access_delete, name='budget-access-delete'),
    
    # UnitTest exists
    path('budget-access/user/<int:user_id>/', budget_access_by_user, name='budget-access-by-user'),
    path('budget-access/budget/<int:budget_id>/', budget_access_by_budget, name='budget-access-by-budget'),

]

