from django.db import models

class Control(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_integer = models.IntegerField(null=True, blank=True)


