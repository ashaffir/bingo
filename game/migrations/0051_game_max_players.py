# Generated by Django 3.1 on 2021-02-01 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0050_remove_album_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='max_players',
            field=models.IntegerField(default=5),
        ),
    ]
