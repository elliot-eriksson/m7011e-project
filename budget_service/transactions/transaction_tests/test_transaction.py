import json
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from budget.models import Budget, BudgetAccess, BudgetRole
from transactions.models import Transaction

class TransactionTestCase(APITestCase):
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

        self.transaction = Transaction.objects.create(
            budget=self.budget,
            description="Test Transaction",
            amount=100,
            category="expense",
            date="2025-01-01",
            user=self.owner.id
        )
        
#############################################OWNER############################################################
    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_create_transaction_as_owner(self, mock_validate_token):
        # Mock token validation
        mock_validate_token.side_effect = lambda request: request

        # Log in as owner
        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()

        response = self.client.post(
            f"/api/transactions/",
            data=json.dumps({
                "budget": self.budget.id,
                "amount": 100,
                "description": "Test Income",
                "category": "income",
                "date": "2025-01-01",
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        # Verify the transaction was created
        self.assertTrue(Transaction.objects.filter(description="Test Income").exists(), "Transaction was not created")

        self.budget.refresh_from_db()
        self.assertEqual(self.budget.currentAmount, 1000)

    

    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_transaction_as_owner(self, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request

        # Log in as owner
        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()

        response = self.client.get(f"/api/transactions/{self.transaction.id}/")
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "budget": 1,   
            "description": "Test Transaction",
            "amount": "100.00",
            "category": "expense",
            "date": "2025-01-01",      
        }
        self.assertEqual(response.json(), expected_response)

        response = self.client.put(
            f"/api/transactions/{self.transaction.id}/",
            data=json.dumps({
                "amount": 200,

            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, 200)

        response = self.client.delete(f"/api/transactions/{self.transaction.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Transaction.objects.filter(description="Test Transaction").exists())

    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_transactions_budget_owner(self, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request

        # Log in as owner
        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()

        response = self.client.get(f"/api/transactions/by-budget/{self.budget.id}/")
        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                "budget": 1,   
                "description": "Test Transaction",
                "amount": "100.00",
                "category": "expense",
                "date": "2025-01-01",      
            }
        ]
        self.assertEqual(response.json(), expected_response)


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
        self.budget.refresh_from_db()

        response = self.client.get(f"/api/transactions/by-budget/{self.budget.id}/")
        self.assertEqual(response.status_code, 404)



    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_transactions_user_owner(self, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request

        # Log in as owner
        self.client.force_login(self.owner)

        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()

        response = self.client.get(f"/api/transactions/by-user/{self.owner.id}/")
        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                "budget": 1,   
                "description": "Test Transaction",
                "amount": "100.00",
                "category": "expense",
                "date": "2025-01-01",      
            }
        ]
        self.assertEqual(response.json(), expected_response)

        response = self.client.get(f"/api/transactions/by-user/{self.admin.id}/")
        self.assertEqual(response.status_code, 401)

#############################################ADMIN############################################################
    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_create_transaction_as_admin(self, mock_validate_token):
        # Mock token validation
        mock_validate_token.side_effect = lambda request: request

        # Log in as owner
        self.client.force_login(self.admin)

        session = self.client.session
        session['user_id'] = self.admin.id
        session.save()

        response = self.client.post(
            f"/api/transactions/",
            data=json.dumps({
                "budget": self.budget.id,
                "amount": 100,
                "description": "Test admin Income",
                "category": "income",
                "date": "2025-01-01",
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        # Verify the transaction was created
        self.assertTrue(Transaction.objects.filter(description="Test admin Income").exists(), "Transaction was not created")

        self.budget.refresh_from_db()
        self.assertEqual(self.budget.currentAmount, 1000)

    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_transaction_as_admin(self, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request

        # Log in as owner
        self.client.force_login(self.admin)

        session = self.client.session
        session['user_id'] = self.admin.id
        session.save()

        response = self.client.get(f"/api/transactions/{self.transaction.id}/")
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "budget": 1,   
            "description": "Test Transaction",
            "amount": "100.00",
            "category": "expense",
            "date": "2025-01-01",      
        }
        self.assertEqual(response.json(), expected_response)

        response = self.client.put(
            f"/api/transactions/{self.transaction.id}/",
            data=json.dumps({
                "amount": 200,

            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, 200)

        response = self.client.delete(f"/api/transactions/{self.transaction.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Transaction.objects.filter(description="Test Transaction").exists())

    @patch("budget_service.auth_service.AuthService.validate_token")
    def test_transactions_budget_admin(self, mock_validate_token):
        mock_validate_token.side_effect = lambda request: request

        # Log in as owner
        self.client.force_login(self.admin)

        session = self.client.session
        session['user_id'] = self.admin.id
        session.save()

        response = self.client.get(f"/api/transactions/by-budget/{self.budget.id}/")
        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                "budget": 1,   
                "description": "Test Transaction",
                "amount": "100.00",
                "category": "expense",
                "date": "2025-01-01",      
            }
        ]
        self.assertEqual(response.json(), expected_response)

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
        self.budget.refresh_from_db()

        response = self.client.get(f"/api/transactions/by-budget/{self.budget.id}/")
        self.assertEqual(response.status_code, 404)