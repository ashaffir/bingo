# Generated by Django 3.1 on 2021-01-03 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0039_remove_displaypicture_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='matched',
            field=models.BooleanField(default=False),
        ),
    ]
