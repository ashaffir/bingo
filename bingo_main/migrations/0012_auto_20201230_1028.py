# Generated by Django 3.1 on 2020-12-30 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo_main', '0011_auto_20201227_0603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentpage',
            name='language',
            field=models.CharField(choices=[('Hebrew', 'he'), ('Spanish', 'es'), ('English', 'en')], default='English', max_length=20),
        ),
    ]
