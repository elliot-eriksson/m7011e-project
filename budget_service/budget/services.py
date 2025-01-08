from . producer import publish
from rest_framework.response import Response
from rest_framework import status
from .models import BudgetAccess, BudgetRole
from django.utils.crypto import get_random_string


class BudgetAccessService:
    def __init__(self, request):
        self.request = request

    def check_budget_access(self, role, access):
        if not access.has_permission('invite_users'):
            return Response({'error': 'You do not have permission to invite users.'}, status=status.HTTP_403_FORBIDDEN)

        if role == BudgetRole.admin and not access.has_permission('invite_user_as_admin'):
            return Response({'error': 'You do not have permission to invite admins.'}, status=status.HTTP_403_FORBIDDEN)

        if role not in [BudgetRole.admin, BudgetRole.member]:
            return Response({'error': 'Invalid role.'}, status=status.HTTP_400_BAD_REQUEST)

    def publish_email_invitation(self, user_email, budget, role, user_id):
        # Generate slugToken
        while True:
            slugToken = get_random_string(length=16, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            if not BudgetAccess.objects.filter(slug=slugToken).exists():
                break

        # Prepare payload for the email
        payload = {
            'recipient_email': user_email,
            'budget_name': budget.budgetName,
            'role': role,
            'inviter_name': self.request.session.get('username'),
            'inviter_id' : self.request.session.get('user_id'),
            'recipient_id': user_id,
            'token': slugToken
        }

        try:
            publish('send.email', payload, 'send_email_invitations')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return slugToken

    def create_budget_access(self, access, budget, user_ID, role):
        try:
            budgetAccess = BudgetAccess.objects.filter(user=user_ID, budget=budget, accepted=True).first()
            if budgetAccess:
                if budgetAccess.accessLevel == role:
                    return Response({'error': 'User already has access to this budget.'}, status=status.HTTP_400_BAD_REQUEST)
                elif access.has_permission('invite_user_as_admin'):
                    budgetAccess.accessLevel = role
                    budgetAccess.save()
                    return Response({'message': 'User access level updated successfully.'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
