# Generated by Django 3.1 on 2021-01-02 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0038_displaypicture_matched'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='displaypicture',
            name='player',
        ),
    ]
