from django.db import models
from users.models import User

class Plan(models.Model):
 
    name = models.CharField(max_length=20, null=True, blank=True)
    players = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    stripe_id = models.CharField(max_length=100, null=True, blank=True)

    price_monthly = models.IntegerField(default=0)
    price_monthly_stripe_id = models.CharField(max_length=100, null=True, blank=True)
    price_yearly = models.IntegerField(default=0)
    price_yearly_stripe_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)