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
            slug="Test-budget"
        )

        # Assign roles
        BudgetAccess.objects.create(budget=self.budget, user=self.owner.id, accessLevel=BudgetRole.owner, accepted=True, slug="owner", username=self.owner.username)
        BudgetAccess.objects.create(budget=self.budget, user=self.admin.id, accessLevel=BudgetRole.admin, accepted=True, slug="admin", username=self.admin.username)
        BudgetAccess.objects.create(budget=self.budget, user=self.member.id, accessLevel=BudgetRole.member, accepted=True, slug="member", username=self.member.username)

    # Test for path('budget/<int:budget_id>/', views.budget_access_by_budget, name="budget_access_by_budget"), get
    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_budget_access_by_budget(self, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request
        # Test owner's ability to update the budget
        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()

        response = self.client.get(
            f"/api/budget-access/budget/{self.budget.slug}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        expected_response = [{
            "accessLevel": "owner",
            "slug": "owner",
            "accepted": True,
            "username": self.owner.username,
            }]
        expected_response.append(
            {
            "accessLevel": "admin",
            "slug": "admin",
            "accepted": True,
            "username": self.admin.username,
            }
        )
        expected_response.append(
            {
            "accessLevel": "member",
            "slug": "member",
            "accepted": True,
            "username": self.member.username,
            }
        )

        self.assertEqual(response.json(), expected_response)

        session['user_id'] = self.member.id
        session.save()
        response = self.client.get(
            f"/api/budget-access/budget/{self.budget.slug}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    # Test for path('budget-access/user/<int:user_id>/', budget_access_by_user, name='budget-access-by-user'),
    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_budget_access_by_user(self, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request
        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session['username'] = self.owner.username
        session.save()

        response = self.client.get(
            f"/api/budget-access/user/{self.owner.username}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        expected_response = [{
            "accessLevel": "owner",
            "slug": "owner",
            "accepted": True,
            "username": self.owner.username,
            }]
        self.assertEqual(response.json(), expected_response)

        response = self.client.get(
            f"/api/budget-access/user/{self.member.username}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    # Test for path('budget-access/<int:budget_id>/', views.budget_access_detail, name="budget_access_detail"),
    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_budget_access_detail_get(self, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request
        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()

        response = self.client.get(
            f"/api/budget-access/{self.budget.slug}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "accessLevel": "owner",
            "slug": "owner",
            "accepted": True,
            "username": self.owner.username,
        }
        self.assertEqual(response.json(), expected_response)

        session['user_id'] = self.testUser.id
        session.save()

        response = self.client.get(
            f"/api/budget-access/{self.budget.slug}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
    
    # Test for path('budget-access/<int:budget_id>/', views.budget_access_detail, name="budget_access_detail"),
    @patch("budget_service.auth_service.AuthService.validate_token")
    @patch("budget.views.getUserID")
    def test_budget_access_detail_put(self, mock_getUserID, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request
        mock_getUserID.return_value = (4, "test@example.com")
        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()

        BudgetAccess.objects.create(budget=self.budget, user=self.testUser.id, accessLevel=BudgetRole.member, accepted=True, slug="testUser")


        response = self.client.put(
            f"/api/budget-access/{self.budget.slug}/",
            data=json.dumps({
                "accessLevel": BudgetRole.admin,
                "username": self.testUser.username
                }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "message": "Access level updated successfully.",
        }
        self.assertEqual(response.json(), expected_response)

        session['user_id'] = self.admin.id
        session.save()

        self.testUser2 = User.objects.create_user(username="testUser2", password="test_pass2")
        BudgetAccess.objects.create(budget=self.budget, user=self.testUser2.id, accessLevel=BudgetRole.member, accepted=True, slug="testUser2")


        response = self.client.put(
            f"/api/budget-access/{self.budget.slug}/",
            data=json.dumps({
                "accessLevel": BudgetRole.admin,
                "username": self.testUser.username
                }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)

    # Test for path('budget-access/<int:budget_id>/', views.budget_access_detail, name="budget_access_detail"),
    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_budget_access_detail_delete(self, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request
        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()

        response = self.client.delete(
            f"/api/budget-access/{self.budget.slug}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

        session['user_id'] = self.admin.id
        session.save()

        response = self.client.delete(
            f"/api/budget-access/{self.budget.slug}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)

        self.assertFalse(BudgetAccess.objects.filter(user=self.admin.id, budget=self.budget).exists())

    # Test for path('budget-access/delete/<int:budget_id>/<str:username>/', views.budget_access_delete, name="budget_access_delete"),
    @patch("budget_service.auth_service.AuthService.validate_token")
    @patch("budget.views.getUserID") 
    def test_budget_access_delete(self, mock_getUserID, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request
        mock_getUserID.return_value = (1, "test@example.com")

        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()

        response = self.client.delete(
            f"/api/budget-access/delete/{self.budget.slug}/{self.owner.username}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

        mock_getUserID.return_value = (2, "test@example.com")

        session['user_id'] = self.admin.id
        session.save()

        response = self.client.delete(
            f"/api/budget-access/delete/{self.budget.slug}/{self.admin.username}/",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)

        session['user_id'] = self.owner.id
        session.save()

        response = self.client.delete(
            f"/api/budget-access/delete/{self.budget.slug}/{self.member.username}/",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    # Test for path('budget-access/budget/<int:budget_id>/', views.budget_access_detail_invite, name="budget_access_detail_invite"),
    @patch("budget_service.auth_service.AuthService.validate_token")
    @patch("budget.services.BudgetAccessService.publish_email_invitation")
    @patch("budget.views.getUserID") 
    def test_budget_access_detail_invite(self, mock_getUserID, mock_publish_email_invitation, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request
        mock_publish_email_invitation.return_value = "SlugStuff"
        mock_getUserID.return_value = (4, "new_user@example.com")

        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()

        response = self.client.post(
            f"/api/budget-access/budget/{self.budget.slug}/",
            data=json.dumps({
                "user": "new_user",
                "email": "new_user@example.com",
                "role": BudgetRole.member}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200, "Owner invites a new user with roll member")
        self.assertTrue(BudgetAccess.objects.filter(user=4, budget=self.budget, accessLevel=BudgetRole.member).exists())

        #Admin invites a new user 

        self.client.force_login(self.admin)

        session = self.client.session
        session['user_id'] = self.admin.id
        session.save()

        response = self.client.post(
            f"/api/budget-access/budget/{self.budget.slug}/",
            data=json.dumps({
                "user": "new_admin",
                "email": "new_admin@example.com",
                "role": BudgetRole.admin}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403, "Admin cannot invite a admins")

        #Member invites a new user
        self.client.force_login(self.member)

        session = self.client.session
        session['user_id'] = self.member.id
        session.save()

        response = self.client.post(
            f"/api/budget-access/budget/{self.budget.slug}/",
            data=json.dumps({
                "user": "new_member",
                "email": "new_member@exmaple.com",
                "accessLevel": BudgetRole.member}),
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 403, "Member cannot invite a new user")

# test for path('invitations/accept/<str:token>/', views.accept_invitation, name="accept_invitation"),
class BudgetInvationAcceptTest(APITestCase):
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
            slug="Test-budget"
        )

        BudgetAccess.objects.create(budget=self.budget, user=self.owner.id, accessLevel=BudgetRole.owner, accepted=True, slug="owner")
        BudgetAccess.objects.create(budget=self.budget, user=self.admin.id, accessLevel=BudgetRole.admin, accepted=False, slug="SlugStuff")

    def test_budget_invitation_accept(self):

        response = self.client.get(
            f"/api/invitations/accept/SlugStuff",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(BudgetAccess.objects.filter(user=self.admin.id, budget=self.budget, accessLevel=BudgetRole.admin, accepted=True).exists())




        