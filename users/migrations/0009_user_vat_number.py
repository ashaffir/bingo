# Generated by Django 3.1 on 2020-11-06 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20201106_0729'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='vat_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]