# Generated by Django 3.1 on 2021-02-01 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20210201_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='max_players',
            field=models.IntegerField(default=5),
        ),
    ]