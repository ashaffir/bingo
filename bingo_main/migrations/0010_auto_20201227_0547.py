# Generated by Django 3.1 on 2020-12-27 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo_main', '0009_contentpage_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentpage',
            name='language',
            field=models.CharField(choices=[('he', 'he'), ('en', 'en')], default='en', max_length=20),
        ),
    ]
