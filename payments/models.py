from django.db import models
from users.models import User

class Payment(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=True)
    amount = models.FloatField(null=True, default=0.0)

    def __str__(self):
        return str(self.date) + " " + str(self.amount)

