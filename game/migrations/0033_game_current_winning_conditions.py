# Generated by Django 3.1 on 2020-12-25 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0032_album_public_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='current_winning_conditions',
            field=models.CharField(blank=True, default='bingo', max_length=10, null=True),
        ),
    ]
