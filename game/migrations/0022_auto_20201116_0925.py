# Generated by Django 3.1 on 2020-11-16 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0021_board_boad_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='boad_id',
            new_name='board_id',
        ),
    ]