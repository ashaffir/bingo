# Generated by Django 3.1 on 2021-01-01 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_payment_charge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='charge',
            new_name='total_charge',
        ),
    ]