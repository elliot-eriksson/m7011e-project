from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from budget_service.auth_service import AuthService
from budget.models import Budget, BudgetAccess


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field= 'slug'

    def dispatch(self, request, *args, **kwargs):
        request = AuthService.validate_token(request)
        return super().dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        budget = Budget.objects.get(slug=self.kwargs['slug'])

        access = BudgetAccess.objects.get(user=self.request.session.get('user_id'), budget=budget)
        if not access.has_permission('add_transaction'):
            return Response("Unauthorized to add transaction for this budget", status=401)
        
        data = request.data.copy()
        data['budget'] = budget.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.session.get('user_id'), budget=budget)
        return Response(serializer.data, status=201)

    def retrieve(self, request, slug=None):
        transaction = get_object_or_404(Transaction, slug=slug)
        access = get_object_or_404(BudgetAccess, user=request.session.get('user_id'), budget=transaction.budget.id)
        if not access.has_permission('view_transactions'):
            return Response("Unauthorized to view transaction for this budget", status=401)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


    def listByUser(self, request, username=None):
        if username != request.session.get('username'):
            return Response("Unauthorized", status=401)
        transactions = Transaction.objects.filter(user=request.session.get('user_id'))
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def listByBudget(self, request, slug=None):
        budget = Budget.objects.get(slug=slug)
        access = get_object_or_404(BudgetAccess, user=request.session.get('user_id'), budget=budget)
        if not access.has_permission('view_transactions'):
            return Response("Unauthorized to view transaction for this budget", status=401)
        transactions = Transaction.objects.filter(budget=budget)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    def update(self, request, slug=None):
        transaction = get_object_or_404(Transaction, slug=slug)
        access = get_object_or_404(BudgetAccess, user=request.session.get('user_id'), budget=transaction.budget.id)
        if not access.has_permission('edit_transaction'):
            return Response("Unauthorized to edit transaction for this budget", status=401)

        serializer = self.get_serializer(transaction, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    def destroy(self, request, slug=None):
        transaction = get_object_or_404(Transaction, slug=slug)
        access = get_object_or_404(BudgetAccess, user=request.session.get('user_id'), budget=transaction.budget.id)
        if not access.has_permission('delete_transaction'):
            return Response("Unauthorized to delete transaction for this budget", status=401)
        return super().destroy(request, slug)
 
                

    