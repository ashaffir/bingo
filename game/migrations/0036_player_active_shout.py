# Generated by Django 3.1 on 2020-12-29 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0035_player_bingo_shouts'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='active_shout',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
