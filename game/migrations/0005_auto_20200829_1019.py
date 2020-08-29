# Generated by Django 3.1 on 2020-08-29 10:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20200829_1011'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'verbose_name': 'Album', 'verbose_name_plural': 'Albums'},
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.album')),
            ],
        ),
    ]
