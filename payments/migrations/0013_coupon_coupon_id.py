# Generated by Django 3.1 on 2021-02-02 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0012_auto_20210201_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='coupon_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]