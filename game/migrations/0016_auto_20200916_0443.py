# Generated by Django 3.1 on 2020-09-16 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_auto_20200915_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='pictures_pool',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='shown_pictures',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
