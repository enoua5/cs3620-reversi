# Generated by Django 2.2 on 2022-11-23 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_game_board_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
