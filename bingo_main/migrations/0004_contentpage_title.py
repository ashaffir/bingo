# Generated by Django 3.1 on 2020-11-10 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo_main', '0003_auto_20201105_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentpage',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]