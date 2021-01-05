# Generated by Django 3.1 on 2021-01-01 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_payment_payment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_id', models.CharField(blank=True, max_length=30, null=True)),
                ('discount', models.FloatField(default=0.0)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]