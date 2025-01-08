from django.urls import path

from .views import *

budget_list = BudgetViewSet.as_view({'get': 'list', 'post': 'create'})
budget_detail = BudgetViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

# BudgetAccessViewSet URLs
budget_access_detail = BudgetAccessViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
budget_access_delete = BudgetAccessViewSet.as_view({'delete': 'deleteBudgetAccess'})

budget_access_by_user = BudgetAccessViewSet.as_view({'get': 'listBudgetAccessByUser'})
budget_access_by_budget = BudgetAccessViewSet.as_view({'get': 'listBudgetAccessByBudget', 'post': 'addBudgetAccess'})

budget_accept_invitation = BudgetInvitationAcceptViewSet.as_view({'get': 'accept_invitation'})

urlpatterns = [
    path('budgets/', budget_list, name='budget-list'),
    path('budgets/<slug:slug>/', budget_detail, name='budget-detail'),

    path('invitations/accept/<str:token>/', budget_accept_invitation, name='budget_accept_invitation'),
    
    path('budget-access/<slug:slug>/', budget_access_detail, name='budget-access-detail'),
    path('budget-access/delete/<slug:slug>/<str:username>/', budget_access_delete, name='budget-access-delete'),
    path('budget-access/user/<str:username>/', budget_access_by_user, name='budget-access-by-user'),
    path('budget-access/budget/<slug:slug>/', budget_access_by_budget, name='budget-access-by-budget'),

]

