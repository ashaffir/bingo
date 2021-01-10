from django import forms
from django.forms import ModelForm

from .models import Newsletter

class NewsletterForm(forms.ModelForm):
    # fname = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control rounded-1'}))
    # lname = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control rounded-1'}))
    # email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control rounded-1'}))
    # subject = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control rounded-1'}))
    # message = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40,'class': 'form-control rounded-1'}))
    
    class Meta:
        model = Newsletter
        # fields = ['fname','lname','email','subject','message',]
        fields = '__all__'
