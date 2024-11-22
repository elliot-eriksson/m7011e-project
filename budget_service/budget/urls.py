from django.urls import path

from .views import BudgetViewSet, UserAPIView

urlpatterns = [
    path('budgets/', BudgetViewSet.as_view({
        'get': 'listBudgets',
        'post': 'createBudget'
    })),
    path('budgets/<int:pk>/', BudgetViewSet.as_view({
        'get': 'getBudget',
        'put': 'updateBudget',
        'delete': 'deleteBudget'
    })),
    path('users/', UserAPIView.as_view())


]