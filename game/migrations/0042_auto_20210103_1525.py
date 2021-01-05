# Generated by Django 3.1 on 2021-01-03 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0041_delete_displaypicture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='matched',
        ),
        migrations.CreateModel(
            name='DisplayPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.IntegerField(default=True, null=True)),
                ('matched', models.BooleanField(default=False)),
                ('board', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.board')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.picture')),
            ],
        ),
    ]