from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField( max_digits=20, decimal_places=2, default=0)
    def __str__(self):
        return self.balance

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now=True)
    amount = models.DecimalField( max_digits=10, decimal_places=2)
    def save(self, *args, **kwargs):
        wallet = Wallet.objects.filter(user = self.user).first()
        wallet.balance += self.amount
        wallet.save()
        return super().save()
    def __str__(self):
        return self.amount
    
class Expence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now=True)
    amount = models.DecimalField( max_digits=10, decimal_places=2)
    def save(self, *args, **kwargs):
        wallet = Wallet.objects.filter(user = self.user).first()
        wallet.balance -= self.amount
        wallet.save()
        return super().save()
    def __str__(self):
        return self.amount
    

    

