# Generated by Django 2.2 on 2022-12-08 22:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0006_game_elo_transferred'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenger_is_X', models.BooleanField(default=True)),
                ('send_time', models.DateTimeField(auto_now_add=True)),
                ('board_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.BoardTemplate')),
                ('challenged', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to=settings.AUTH_USER_MODEL)),
                ('challenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]