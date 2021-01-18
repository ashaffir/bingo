# Generated by Django 3.1 on 2021-01-16 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_user_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='coupons_used',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile_pics/profile.jpg', null=True, upload_to='profile_pics'),
        ),
    ]