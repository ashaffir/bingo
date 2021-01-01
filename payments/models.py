from django.db import models
from users.models import User

class Payment(models.Model):
    PAYMENT_TYPES = (
        ('PayPal', 'PayPal'),
        ('Credit Card', 'Credit Card'),
    )
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=True)
    amount = models.FloatField(null=True, default=0.0)
    invoice_slug = models.CharField(max_length=120, null=True, blank=True)
    invoice_pdf	= models.FileField(upload_to='invoices/', null=True, blank=True)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPES, null=True, blank=True)
    def __str__(self):
        return str(self.date) + " " + str(self.amount)

