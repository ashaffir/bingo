# Generated by Django 3.1 on 2020-09-04 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_stripe_customer_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]