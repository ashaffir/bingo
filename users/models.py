from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

class User(AbstractUser):
    username = models.CharField(max_length=200, blank=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, blank=False)
    phone = models.CharField(max_length=100, null=True, blank=True)
    paypal = models.CharField(max_length=100, null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)
    europeCitizenship = models.BooleanField()
    first_name = models.CharField('First Name', max_length=255, blank=True,
                                  null=False)
    last_name = models.CharField('Last Name', max_length=255, blank=True,
                                 null=False)
                                 
    # require the email to be the unique identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
