# Generated by Django 3.1 on 2020-09-16 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20200916_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winning_conditions',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
