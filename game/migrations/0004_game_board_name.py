# Generated by Django 2.2 on 2022-11-22 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_game_board_string'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='board_name',
            field=models.CharField(default='[BOARD]', max_length=50),
            preserve_default=False,
        ),
    ]