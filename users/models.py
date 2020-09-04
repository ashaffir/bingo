from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse

from rest_framework.authtoken.models import Token
from django_rest_passwordreset.signals import reset_password_token_created

# from .utils import send_mail
from django.core.mail import send_mail  

class User(AbstractUser):
    username = models.CharField(max_length=200, blank=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, blank=False)
    phone = models.CharField(max_length=100, null=True, blank=True)
    paypal = models.CharField(max_length=100, null=True, blank=True)
    balance = models.FloatField(null=True, blank=True, default=0)
    europeCitizenship = models.BooleanField(null=True, blank=True)
    first_name = models.CharField('First Name', max_length=255, blank=True,
                                  null=False)
    last_name = models.CharField('Last Name', max_length=255, blank=True,
                                 null=False)

    stripe_customer_key = models.CharField(max_length=100, null=True, blank=True)                                 
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

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
