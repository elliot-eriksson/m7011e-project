import json
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from budget.models import Budget, BudgetAccess, BudgetRole



class BudgetAccessTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # Create users
        self.owner = User.objects.create_user(username="owner", password="owner_pass")
        self.admin = User.objects.create_user(username="admin", password="admin_pass")
        self.member = User.objects.create_user(username="member", password="member_pass")
        self.testUser = User.objects.create_user(username="testUser", password="test_pass")
        
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

    # @patch("budget_service.auth_service.AuthService.validate_token")
    # def test_budget_access_by_budget(self, mock_validate_token):
    #     mock_validate_token.side_effect = lambda request: request
    #     # Test owner's ability to update the budget
    #     self.client.force_login(self.owner)

    #     session = self.client.session
    #     session['user_id'] = self.owner.id
    #     session.save()

    #     response = self.client.get(
    #         f"/api/budget-access/budget/{self.budget.id}/",
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 200)

    #     expected_response = [{
    #         "id": 1,
    #         "user": 1,
    #         "accessLevel": "owner",
    #         "slug": None,
    #         "accepted": True,
    #         "budget": self.budget.id
    #         }]
    #     expected_response.append(
    #         {
    #         "id": 2,
    #         "user": 2,
    #         "accessLevel": "admin",
    #         "slug": None,
    #         "accepted": True,
    #         "budget": self.budget.id
    #         }
    #     )
    #     expected_response.append(
    #         {
    #         "id": 3,
    #         "user": 3,
    #         "accessLevel": "member",
    #         "slug": None,
    #         "accepted": True,
    #         "budget": self.budget.id
    #         }
    #     )

    #     self.assertEqual(response.json(), expected_response)

    #     session['user_id'] = self.member.id
    #     session.save()
    #     response = self.client.get(
    #         f"/api/budget-access/budget/{self.budget.id}/",
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 403)

    # @patch("budget_service.auth_service.AuthService.validate_token")
    # def test_budget_access_by_user(self, mock_validate_token):
    #     mock_validate_token.side_effect = lambda request: request
    #     self.client.force_login(self.owner)

    #     session = self.client.session
    #     session['user_id'] = self.owner.id
    #     session.save()

    #     response = self.client.get(
    #         f"/api/budget-access/user/{self.owner.id}/",
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 200)

    #     expected_response = [{
    #         "id": 1,
    #         "user": 1,
    #         "accessLevel": "owner",
    #         "slug": None,
    #         "accepted": True,
    #         "budget": self.budget.id
    #         }]
    #     self.assertEqual(response.json(), expected_response)

    #     response = self.client.get(
    #         f"/api/budget-access/user/{self.member.id}/",
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 403)

    # @patch("budget_service.auth_service.AuthService.validate_token")
    # def test_budget_access_detail_get(self, mock_validate_token):
    #     mock_validate_token.side_effect = lambda request: request
    #     self.client.force_login(self.owner)

    #     session = self.client.session
    #     session['user_id'] = self.owner.id
    #     session.save()

    #     response = self.client.get(
    #         f"/api/budget-access/{self.budget.id}/",
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 200)

    #     expected_response = {
    #         "id": 1,
    #         "user": 1,
    #         "accessLevel": "owner",
    #         "slug": None,
    #         "accepted": True,
    #         "budget": self.budget.id
    #     }
    #     self.assertEqual(response.json(), expected_response)

    #     session['user_id'] = self.testUser.id
    #     session.save()

    #     response = self.client.get(
    #         f"/api/budget-access/{self.budget.id}/",
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 404)
    

    # TODO: Behövs en till patch för att test då vi skickar email tror jag Elliot fixar
    # @patch("budget_service.auth_service.AuthService.validate_token")
    # @patch("budget.services.BudgetAccessService.publish_email_invitation")
    # @patch("budget_service.user_lookup.getUserID") 
    # def test_budget_access_detail_put(self, mock_validate_token):
    #     mock_validate_token.side_effect = lambda request: request
    #     self.client.force_login(self.owner)

    #     session = self.client.session
    #     session['user_id'] = self.owner.id
    #     session.save()

    #     response = self.client.put(
    #         f"/api/budget-access/{self.budget.id}/",
    #         data=json.dumps({"accessLevel": "member",
    #                             "user": self.testUser.id,
    #                             "email": self.testUser.email,
    #                          }),
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 200)

    #     expected_response = {
    #         "id": 1,
    #         "user": 1,
    #         "accessLevel": "member",
    #         "slug": None,
    #         "accepted": True,
    #         "budget": self.budget.id
    #     }
    #     self.assertEqual(response.json(), expected_response)

    #     session['user_id'] = self.member.id
    #     session.save()

    #     response = self.client.put(
    #         f"/api/budget-access/{self.budget.id}/",
    #         data=json.dumps({"accessLevel": "admin"}),
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 403)

    # TODO: Behövs en till patch för att testa dvs getUSERID Elliot fixar

    @patch("budget_service.auth_service.AuthService.validate_token")
    @patch("budget.views.getUserID") 
    def test_budget_access_detail_delete(self, mock_getUserID, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request
        mock_getUserID.return_value = (1, "test@example.com")

        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()

        response = self.client.delete(
            f"/api/budget-access/delete/{self.budget.id}/{self.owner.username}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

        mock_getUserID.return_value = (2, "test@example.com")

        session['user_id'] = self.admin.id
        session.save()

        response = self.client.delete(
            f"/api/budget-access/delete/{self.budget.id}/{self.admin.username}/",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)

        session['user_id'] = self.owner.id
        session.save()

        response = self.client.delete(
            f"/api/budget-access/delete/{self.budget.id}/{self.member.username}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

