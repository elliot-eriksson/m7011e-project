### Elliot Testar
import json
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from budget.models import Budget, BudgetAccess, BudgetRole



# class BudgetCaseTest(APITestCase):

#     def setUp(self):
#         self.client = APIClient()
#         # Create users
#         self.owner = User.objects.create_user(username="owner", password="owner_pass")
#         self.admin = User.objects.create_user(username="admin", password="admin_pass")
#         self.member = User.objects.create_user(username="member", password="member_pass")
        
#         # Create a budget
#         self.budget = Budget.objects.create(
#             budgetName="Test Budget",
#             owner=self.owner.id,
#             budgetAmount=1000,
#             currentAmount=1000,
#             category="General",
#             startDate="2025-01-01",
#             endDate="2025-12-31",
#         )

#         # Assign roles
#         BudgetAccess.objects.create(budget=self.budget, user=self.owner.id, accessLevel=BudgetRole.owner, accepted=True)
#         BudgetAccess.objects.create(budget=self.budget, user=self.admin.id, accessLevel=BudgetRole.admin, accepted=True)
#         BudgetAccess.objects.create(budget=self.budget, user=self.member.id, accessLevel=BudgetRole.member, accepted=True)

#     @patch("budget_service.auth_service.AuthService.validate_token")
#     def test_owner_permissions(self, mock_validate_token):
#         # mock_validate.return_value = True
#         mock_validate_token.side_effect = lambda request: request
#         # Test owner's ability to update the budget
#         self.client.force_login(self.owner)

#         session = self.client.session
#         session['user_id'] = self.owner.id
#         session.save()

#         response = self.client.put(
#             f"/api/budgets/{self.budget.id}/",
#             data=json.dumps({
#                 "budgetName": "Updated Budget",
#                 "budgetAmount": 1500,
#             }),
#             content_type="application/json"
#         )
#         self.assertEqual(response.status_code, 200)

#         expected_response = {
#             "budgetName":"Updated Budget",
#             "budgetAmount":"1500.00",
#             "currentAmount":"1000.00",
#             "category":"General",
#             "startDate":"2025-01-01",
#             "endDate":"2025-12-31"
#         }

#         response = self.client.get(f"/api/budgets/{self.budget.id}/")
#         self.assertEqual(response.json(), expected_response)

        
#         response = self.client.delete(f"/api/budgets/{self.budget.id}/")
#         self.assertEqual(response.status_code, 204)

#     @patch("budget_service.auth_service.AuthService.validate_token")
#     def test_admin_permissions(self, mock_validate_token):
#         # Admin can edit but not delete the budget
#         self.client.force_login(self.admin)

#         mock_validate_token.side_effect = lambda request: request

#         session = self.client.session
#         session['user_id'] = self.admin.id
#         session.save()

#         response = self.client.put(
#             f"/api/budgets/{self.budget.id}/",
#             data=json.dumps({
#                 "budgetName": "Admin Updated Budget",
#             }),
#             content_type="application/json"
#         )
#         self.assertEqual(response.status_code, 200)

#         expected_response = {
#             "budgetName":"Admin Updated Budget",
#             "budgetAmount":"1000.00",
#             "currentAmount":"1000.00",
#             "category":"General",
#             "startDate":"2025-01-01",
#             "endDate":"2025-12-31"
#         }

#         response = self.client.get(f"/api/budgets/{self.budget.id}/")
#         self.assertEqual(response.json(), expected_response)

#         response = self.client.delete(f"/api/budgets/{self.budget.id}/")
#         self.assertEqual(response.status_code, 403)

#     @patch("budget_service.auth_service.AuthService.validate_token")
#     def test_member_permissions(self, mock_validate_token):
#         self.client.force_login(self.member)

#         mock_validate_token.side_effect = lambda request: request

#         session = self.client.session
#         session['user_id'] = self.member.id
#         session.save()

#         # Member cannot update or delete the budget
#         response = self.client.put(
#             f"/api/budgets/{self.budget.id}/",
#             data=json.dumps({
#                 "budgetName": "Member Updated Budget",
#             }),
#             content_type="application/json"
#         )
#         self.assertEqual(response.status_code, 403)

#         expected_response = {
#             "budgetName":"Test Budget",
#             "budgetAmount":"1000.00",
#             "currentAmount":"1000.00",
#             "category":"General",
#             "startDate":"2025-01-01",
#             "endDate":"2025-12-31"
#         }

#         response = self.client.get(f"/api/budgets/{self.budget.id}/")
#         self.assertEqual(response.json(), expected_response)
        

#         response = self.client.delete(f"/api/budgets/{self.budget.id}/")
#         self.assertEqual(response.status_code, 403)
    
class BudgetListCreateTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # Create users
        self.owner = User.objects.create_user(username="owner", password="owner_pass")
        self.admin = User.objects.create_user(username="admin", password="admin_pass")
        self.member = User.objects.create_user(username="member", password="member_pass")
        
        # Create a budget
        self.budget = Budget.objects.create(
            budgetName="Test Budget",
            owner=self.owner.id,
            budgetAmount=1000,
            currentAmount=1000,
            category="General",
            startDate="2025-01-01",
            endDate="2025-12-31",
        )

        # Assign roles
        BudgetAccess.objects.create(budget=self.budget, user=self.owner.id, accessLevel=BudgetRole.owner, accepted=True)
        BudgetAccess.objects.create(budget=self.budget, user=self.admin.id, accessLevel=BudgetRole.admin, accepted=True)
        BudgetAccess.objects.create(budget=self.budget, user=self.member.id, accessLevel=BudgetRole.member, accepted=True)

    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_create_budget(self, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request
        client = APIClient()
        user = User.objects.create_user(username="testuser", password="testuser_pass")
        client.force_login(user)

        session = client.session
        session['user_id'] = user.id
        session.save()

        response = client.post(
            "/api/budgets/",
            data=json.dumps({
                "budgetName": "Test Budget2",
                "budgetAmount": "1000.00",
                "currentAmount": "500.00",
                "category": "General",
                "startDate": "2025-01-01",
                "endDate": "2025-12-31"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        expected_response = {
            "budgetName":"Test Budget2",
            "budgetAmount":"1000.00",
            "currentAmount":"500.00",
            "category":"General",
            "startDate":"2025-01-01",
            "endDate":"2025-12-31"
        }

        self.assertEqual(response.json(), expected_response)

    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_list_budgets(self, mock_validate_token):
        self.client.force_login(self.admin)

        mock_validate_token.side_effect = lambda request: request

        session = self.client.session
        session['user_id'] = self.admin.id
        session.save()

        response = self.client.get("/api/budgets/")
        self.assertEqual(response.status_code, 200)

        expected_response = [{
            "budgetName":"Test Budget",
            "budgetAmount":"1000.00",
            "currentAmount":"1000.00",
            "category":"General",
            "startDate":"2025-01-01",
            "endDate":"2025-12-31"
        }]

        self.assertEqual(response.json(), expected_response)


        self.budget = Budget.objects.create(
            budgetName="Test Budget2",
            owner=self.owner.id,
            budgetAmount=1000,
            currentAmount=1000,
            category="General",
            startDate="2025-01-01",
            endDate="2025-12-31",
        )

        BudgetAccess.objects.create(budget=self.budget, user=self.admin.id, accessLevel=BudgetRole.admin, accepted=True)

        response = self.client.get("/api/budgets/")
        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
            "budgetName":"Test Budget",
            "budgetAmount":"1000.00",
            "currentAmount":"1000.00",
            "category":"General",
            "startDate":"2025-01-01",
            "endDate":"2025-12-31"
            },
            {
            "budgetName":"Test Budget2",
            "budgetAmount":"1000.00",
            "currentAmount":"1000.00",
            "category":"General",
            "startDate":"2025-01-01",
            "endDate":"2025-12-31"
            }
        ]

        self.assertEqual(response.json(), expected_response)

    
