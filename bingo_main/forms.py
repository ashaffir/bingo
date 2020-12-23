from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from users.models import User
from .models import ContactUs

class HostSignupForm(UserCreationForm):
    # terms_accepted = forms.BooleanField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2', )
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        return user

class ContactForm(forms.ModelForm):
    # fname = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control rounded-1'}))
    # lname = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control rounded-1'}))
    # subject = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control rounded-1'}))
    email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control rounded-1'}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40,'class': 'form-control rounded-1'}))
    
    class Meta:
        model = ContactUs
        fields = ['email','message',]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                "class": "form-control"
            }
        ))
