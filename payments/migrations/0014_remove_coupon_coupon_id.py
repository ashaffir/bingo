# Generated by Django 3.1 on 2021-02-02 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0013_coupon_coupon_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='coupon_id',
        ),
    ]