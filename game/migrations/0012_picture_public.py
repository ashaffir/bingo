# Generated by Django 3.1 on 2020-11-08 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_auto_20201108_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
