from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.generics import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .filters import IncomeFilter, ExpenceFilter 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from accounts.models import IsTokenValid
class IncomeAPIView(ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = IncomeFilter
    ordering_fields = ['time']
    ordering = ['-time'] 

    def get(self, request, *args, **kwargs):
        # Calculate total income for the user (or globally)
        incomes = Income.objects.all()  # You can filter by user if needed
        total_income = sum(income.amount for income in incomes)

        # Get the actual response data (list of incomes)
        response_data = super().get(request, *args, **kwargs).data

        # Add the total income to the response data
        response_data.append({
            'total_income': total_income
        })

        return Response(response_data)

    def perform_create(self, serializer):
        user = self.request.user  # Get the currently authenticated user
        serializer.save(user=user)

class IncomeRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    def perform_create(self, serializer):
        user = self.request.user 
        serializer.save(user=user)

class ExpenceAPIView(ListCreateAPIView):
    queryset = Expence.objects.all()
    serializer_class = ExpenceSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ExpenceFilter
    ordering_fields = ['time']
    ordering = ['-time']

    def get(self, request, *args, **kwargs):
        # Calculate total income for the user (or globally)
        expences = Expence.objects.all()  # You can filter by user if needed
        total_expence = sum(expence.amount for expence in expences)

        # Get the actual response data (list of incomes)
        response_data = super().get(request, *args, **kwargs).data

        # Add the total income to the response data
        response_data.append({
            'total_expence': total_expence
        })

        return Response(response_data)
    def perform_create(self, serializer):
        user = self.request.user 
        serializer.save(user=user)

class ExpenceRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Expence.objects.all()
    serializer_class = ExpenceSerializer
    def perform_create(self, serializer):
        user = self.request.user 
        serializer.save(user=user)

class WalletAPIView(IsAuthenticated,IsTokenValid,ListCreateAPIView):
    permission_classes = [IsTokenValid]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    def perform_create(self, serializer):
        user = self.request.user 
        serializer.save(user=user)

class WalletHistoryAPIView(ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    def get(self, request, *args, **kwargs):
        # Get the current user's wallet
        wallet = Wallet.objects.get(user=request.user)

        # Fetch the last 3 incomes and 3 expenses for the user
        last_three_incomes = Income.objects.filter(user=request.user).order_by('-time')[:3]
        last_three_expenses = Expence.objects.filter(user=request.user).order_by('-time')[:3]

        # Combine the last 3 incomes and expenses
        actions = list(last_three_incomes) + list(last_three_expenses)

        # Sort the combined actions by the date field (latest first)
        actions_sorted = sorted(actions, key=lambda x: x.time, reverse=True)

        # Serialize the actions (we can use either IncomeSerializer or ExpenceSerializer based on the object type)
        actions_data = []
        for action in actions_sorted:
            if isinstance(action, Income):
                serialized_action = IncomeSerializer(action)
            elif isinstance(action, Expence):
                serialized_action = ExpenceSerializer(action)
            actions_data.append(serialized_action.data)

        # Prepare the response data, including the total balance
        response_data = {
            'balance': wallet.balance,
            'last_three_actions': actions_data
        }

        return Response(response_data, status=status.HTTP_200_OK)
