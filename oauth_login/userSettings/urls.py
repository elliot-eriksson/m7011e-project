from django.urls import path
from .views import UserSettingsView

# budget_list = BudgetViewSet.as_view({'get': 'list', 'post': 'create'})

urlpatterns = [
    path('settings/', UserSettingsView.as_view(), name='userSetting'),
]