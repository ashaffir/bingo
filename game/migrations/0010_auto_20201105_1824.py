# Generated by Django 3.1 on 2020-11-05 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_album_board_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='album',
        ),
        migrations.AddField(
            model_name='picture',
            name='album_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='pictures',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
