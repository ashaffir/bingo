from django.db import models
from django.db.models import JSONField
from ckeditor.fields import RichTextField


class Newsletter(models.Model):
    LANGUAGES = (
		('English', 'en'),
		('Hebrew', 'he'),
		('Spanish', 'es'),
	)

    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)
    sent_date = models.DateTimeField(null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    title_1 = models.CharField(max_length=100, null=True, blank=True)
    content_1 = RichTextField(max_length=10000, null=True, blank=True)
    title_2 = models.CharField(max_length=100, null=True, blank=True)
    content_2 = RichTextField(max_length=10000, null=True, blank=True)
    title_3 = models.CharField(max_length=100, null=True, blank=True)
    content_3 = RichTextField(max_length=10000, null=True, blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGES, default='English')
    
    button_text = models.CharField(max_length=20, null=True, blank=True)
    button_link = models.CharField(max_length=200, null=True, blank=True)

    recipients_type = models.CharField(max_length=20, null=True, blank=True)
    recipients = JSONField(blank=True, null=True, default=list)
    recipients_count = models.IntegerField(blank=True, null=True, default=0)

class EmailTemplate(models.Model):
    LANGUAGES = (
		('he', 'he'),
		('en', 'en'),
	)
    name = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = RichTextField(max_length=2000, null=True, blank=True)
    button_text = models.CharField(max_length=20, null=True, blank=True)
    button_link = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGES, default='en')





