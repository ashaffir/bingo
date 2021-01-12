from django.db import models

class Control(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_integer = models.IntegerField(null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

