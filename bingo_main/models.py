from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser

class ContentPage(models.Model):
	LANGUAGES = (
		('Hebrew', 'he'),
		('Spanish', 'es'),
		('English', 'en'),
	)
	name = models.CharField(max_length=100, null=True, blank=True)
	title = models.CharField(max_length=100, null=True, blank=True)
	content = RichTextField(max_length=100000, null=True, blank=True)
	language = models.CharField(max_length=20, choices=LANGUAGES, default='English')
	section = models.CharField(max_length=100, null=True, blank=True)
	active = models.BooleanField(default=True)
	image_id = models.CharField(max_length=200, null=True, blank=True)
	image_1 = models.ImageField(null=True, blank=True, upload_to="content_images", default = 'profile_pics/placeholder.png')
	image_2 = models.ImageField(null=True, blank=True, upload_to="content_images", default = 'profile_pics/placeholder.png')
	video = models.CharField(max_length=200, null=True, blank=True)


	def __str__(self):
	 return self.name

class ContactUs(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

