# Generated by Django 3.1 on 2021-02-01 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_user_stripe_plan_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='stripe_plan_id',
            new_name='stripe_sub_id',
        ),
    ]
