from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['title', 'description', 'time', 'amount']
    

class ExpenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expence
        fields = ['title', 'description', 'time', 'amount']
    
class WalletSerializer(serializers.ModelSerializer):
    incomes = serializers.SerializerMethodField()
    expences = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ['balance', 'incomes', 'expences']

    def get_incomes(self, obj):
        # Fetch incomes related to the wallet's user
        incomes = Income.objects.filter(user = obj.user)  # Adjusted to use `wallet=obj`
        return [
            {
                'id': income.id,
                'amount': str(income.amount),  # You can use str() to format or customize the amount
                'date': income.time,
            }
            for income in incomes
        ]

    def get_expences(self, obj):
        # Fetch expenses related to the wallet's user
        expences = Expence.objects.filter(user = obj.user)  # Adjusted to use `wallet=obj`
        return [
            {
                'id': expence.id,
                'amount': str(expence.amount),  # You can format the amount as needed
                'date': expence.time,
            }
            for expence in expences
        ]
    