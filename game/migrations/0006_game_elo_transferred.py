# Generated by Django 2.2 on 2022-12-08 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_game_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='elo_transferred',
            field=models.IntegerField(null=True),
        ),
    ]
