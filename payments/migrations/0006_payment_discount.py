# Generated by Django 3.1 on 2021-01-01 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='discount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
