import json
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .producer import publish
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .serializers import *
from .models import Budget
from budget_service.auth_service import AuthService
from budget_service.user_lookup import getUserID
from django.utils.crypto import get_random_string
from .services import BudgetAccessService

# Create your views here.
class BudgetViewSet(viewsets.ModelViewSet):

    ##CHANGE
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

    def dispatch(self, request, *args, **kwargs):
        # print("Dispatching request for token validation.")
        # print(f"Request: {request}")
        request = AuthService.validate_token(request)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # print('getting queryset')
        # self.request.user = self.request.user_info.get('user_id')
        self.request.user = self.request.session.get('user_id')
        # print(f"User: {self.request.user}")
        access_entries = BudgetAccess.objects.filter(user=self.request.user)
        # print(f"BudgetAccess entries for user {self.request.user}: {access_entries}")
        # budgets = Budget.objects.filter(owner=self.request.user)
        budgets = Budget.objects.filter(id__in=[access.budget.id for access in access_entries])
        # print(f"Budgets found: {budgets}")

        # print(f"Budgets for user: {Budget.objects.filter(owner=self.request.user)}")
        return budgets
        # return Budget.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        # print('listing budgets')
        # print(f"User ID: {request.session.get('user_id')}")
        request.user = request.session.get('user_id')
        
        response = BudgetAccessViewSet.listBudgetAccessByUser(self, request, request.user)
        serialized_budgets = []

        for r in response.data:
            try:
                # Get the Budget object associated with the budget ID
                budget = Budget.objects.get(id=r['budget'])
                
                # Serialize the Budget object
                serialized_budget = BudgetSerializer(budget)
                serialized_budgets.append(serialized_budget.data)

            except Budget.DoesNotExist:
                print(f"Budget with ID {r['budget']} does not exist.")

        # print(f"List of budgets: {serialized_budgets}")
        # Return the serialized data in a Response object
        return Response(serialized_budgets)

    def update(self, request, *args, **kwargs):
        self.request.user = self.request.session.get('user_id')
        instance = self.get_object()
        access = get_object_or_404(BudgetAccess, user=request.user, budget=instance, accepted=True)
        if not access.has_permission('edit_budget'):
            return Response({'error': 'You do not have permission to edit this budget.'}, status=status.HTTP_403_FORBIDDEN)    
            # Allow partial updates    
        try:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as e:
            print(f"Error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.data)        
        # return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        self.request.user = self.request.session.get('user_id')
        user_id = self.request.user
        serializer.save(owner=user_id)
        # print('creating budget')
        self.createBudgetAccessEntry(serializer.instance, user_id)
        # self.createBudgetAccessEntry(serializer.instance, self.request.user)

    def createBudgetAccessEntry(self, budget, user_id, accessLevel= 'owner', accepted=True):
        #TODO: kanske går att använda denna i addBudgetAccess också
        # print('creating budget access entry')
        budget_access_data = {
            'budget': budget.id,
            'user': user_id,
            'accessLevel': 'owner',
            'accepted': True
        }
        budget_access_serializer = BudgetAccessSerializer(data=budget_access_data)
        budget_access_serializer.is_valid(raise_exception=True)
        budget_access_serializer.save()

    def destroy(self, request, *args, **kwargs):
        self.request.user = self.request.session.get('user_id')
        instance = self.get_object()
        access = get_object_or_404(BudgetAccess, user=request.user, budget=instance)
        if not access.has_permission('delete_budget'):
            return Response({'error': 'You do not have permission to delete this budget.'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class BudgetAccessViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetAccessSerializer

    def dispatch(self, request, *args, **kwargs):
        # print("Dispatching request for token validation.")
        request = AuthService.validate_token(request)
        return super().dispatch(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        self.request.user = self.request.session.get('user_id')
        instance = self.get_object()
        access = get_object_or_404(BudgetAccess, user=request.user, budget=instance)
        return Response(BudgetAccessSerializer(access).data)
    
    def addBudgetAccess(self, request, budget_id=None):
        self.request.user = self.request.session.get('user_id')
        budget = get_object_or_404(Budget, pk=budget_id)
        access = get_object_or_404(BudgetAccess, user=request.user, budget=budget)

        username = request.data.get('username')
        email = request.data.get('email')
        role = request.data.get('role', BudgetRole.member)

        if not username and not email:
            return Response(
                {'error': 'At least one of username or email must be provided.'},
                status=status.HTTP_400_BAD_REQUEST
        )

        budget_access_service = BudgetAccessService(request)

        permission_response = budget_access_service.check_budget_access(role, access)
        if permission_response:
            return permission_response

        try:
            user_ID, user_email = getUserID(username, email)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        access_response = budget_access_service.create_budget_access(access, budget, user_ID, role)
        if access_response:
            return access_response
        
        slugToken = budget_access_service.publish_email_invitation(user_email, budget, role)
        try:
            budget_access_data = {
                'budget': budget.id,
                'user': user_ID,
                'accessLevel': role,
                'slug': slugToken
            }
            budget_access_serializer = BudgetAccessSerializer(data=budget_access_data)
            budget_access_serializer.is_valid(raise_exception=True)
            budget_access_serializer.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'User invited successfully.'})

    def listBudgetAccessByUser(self, request, user_id=None):
        # TODO: ändra till slug
        user = user_id
        if user != request.session.get('user_id'):
            return Response({'error': 'You do not have permission to view that users access.'}, status=status.HTTP_403_FORBIDDEN)
        budgetAccess = BudgetAccess.objects.filter(user=user)
        serializer = BudgetAccessSerializer(budgetAccess, many=True)

        # print(serializer.data)
        return Response(serializer.data)

    def listBudgetAccessByBudget(self, request, budget_id=None):
        request.user = request.session.get('user_id')
        access = get_object_or_404(BudgetAccess, user=request.user, budget=budget_id)
        if not access.has_permission('view_budget_access'):
            return Response({'error': 'You do not have permission to view access to this budget.'}, status=status.HTTP_403_FORBIDDEN)
        budget = Budget.objects.get(id=budget_id)
        budgetAccess = BudgetAccess.objects.filter(budget=budget)
        serializer = BudgetAccessSerializer(budgetAccess, many=True)
        return Response(serializer.data)
    
    #TODO: Behöver mer checks för om du försöker ändra till admin
    def update(self, request, *args, **kwargs):
        self.request.user = self.request.session.get('user_id')
        instance = self.get_object()
        access = get_object_or_404(BudgetAccess, user=request.user, budget=instance)
        username = request.data.get('username')
        role = request.data.get('accessLevel')
        if not username or not role:
            return Response({'error': 'Username and accessLevel must be provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_ID, user_email = getUserID(username, None)
            accessToChange = get_object_or_404(BudgetAccess, user=user_ID, budget=instance)
        except Exception as e:
            return Response({'error': 'User does not have access to this budget.'}, status=status.HTTP_404_BAD_REQUEST)
        if not access.has_permission('edit_access_level'):
            return Response({'error': 'You do not have permission to edit this budget access.'}, status=status.HTTP_403_FORBIDDEN)
        if accessToChange.accessLevel == 'owner':
            return Response({'error': 'Cannot change owner access level.'}, status=status.HTTP_400_BAD_REQUEST)
        if role == 'owner':
            return Response({'error': 'Cannot change access level to owner.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER)

        return Response({'message': 'Access level updated successfully.'})
        
        # return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        try:
            self.request.user = self.request.session.get('user_id')
            instance = self.get_object()
            access = get_object_or_404(BudgetAccess, user=request.user, budget=instance)
            if access.accessLevel == 'owner':
                return Response({'error': 'Cannot delete owner access level, delete budget instead.'}, status=status.HTTP_400_BAD_REQUEST)
            self.perform_destroy(instance)
        except Exception as e:
            return Response({'error': 'You dont have access to that budget'}, status=status.HTTP_404_INTERNAL_SERVER_ERROR)
        return Response({'You have left the budget'},status=status.HTTP_204_NO_CONTENT)

    # TODO: change pk to slug
    def deleteBudgetAccess(self, request, budgetID=None, username=None):
        self.request.user = self.request.session.get('user_id')
        budget = get_object_or_404(Budget, pk=budgetID)
        access = get_object_or_404(BudgetAccess, user=request.user, budget=budget)

        if not access.has_permission('remove_admin') or not access.has_permission('remove_user_access'):
            return Response({'error': 'You do not have permission to delete access to this budget.'}, status=status.HTTP_403_FORBIDDEN)

        user_ID, user_email = getUserID(username, None)

        try:
            budgetAccess = BudgetAccess.objects.filter(user=user_ID, budget=budget).first()
            if not budgetAccess:
                return Response({'error': 'User does not have access to this budget.'}, status=status.HTTP_400_BAD_REQUEST)
            if budgetAccess.accessLevel == 'owner':
                return Response({'error': 'Cannot delete owner access level.'}, status=status.HTTP_400_BAD_REQUEST)
            elif budgetAccess.accessLevel == 'admin' and not access.has_permission('remove_admin'):
                return Response({'error': 'You do not have permission to delete admin access level.'}, status=status.HTTP_403_FORBIDDEN)
            budgetAccess.delete()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'User access deleted successfully.'})
    
class BudgetInvitationAcceptViewSet(viewsets.ModelViewSet):
    queryset = BudgetAccess.objects.all()
    serializer_class = BudgetAccessSerializer

    def accept_invitation(self, request, token=None):
        # Fetch the BudgetAccess object or return a 404
        # print(f"Token: {token}")
        # token = request.data.get('token')
        # print(f"Token: {token}")
        budget_access = get_object_or_404(BudgetAccess, slug=token)
        
        if not token:
            return Response(
                {"error": "Token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Check if access is already accepted
        if budget_access.accepted:
            return Response(
                {"message": "Access already accepted."},
                status=status.HTTP_200_OK
            )

        # Update the accepted field and save
        budget_access.accepted = True
        budget_access.save()

        return Response(
            {"message": "Access accepted successfully."},
            status=status.HTTP_200_OK
        )
        

# class UserAPIView(APIView):
#     def get(self, pk=None):
#         users = get_user_model().objects.all()
#         user = get_user_model().objects.get(id=pk)
#         return Response({'id': user.id})




class UserAPIView(APIView):
    # Use JWT authentication and ensure the user is authenticated
    # authentication_classes = [OAuth2Authentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve user details from the request (decoded from the JWT token)
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,  # Add additional fields as needed
            'email': user.email,
        })