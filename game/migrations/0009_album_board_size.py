# Generated by Django 3.1 on 2020-11-05 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20201105_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='board_size',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
