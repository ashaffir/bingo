# Generated by Django 3.1 on 2021-01-04 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0042_auto_20210103_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='displaypicture',
            name='game_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]