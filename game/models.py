from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BoardTemplate(models.Model):
    name = models.CharField(max_length=50)
    # max_length here allows for a 32x32 board
    board_string = models.CharField(max_length=1056)

    def __str__(self):
        return self.name

class Challenge(models.Model):
    challenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges_sent')
    challenged = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')

    challenger_is_X = models.BooleanField(default=True)
    board_id = models.ForeignKey(BoardTemplate, on_delete=models.CASCADE)

    send_time = models.DateTimeField(auto_now_add=True)


class Game(models.Model):
    first_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_player_in')
    # second is nullable so that an open game can be made
    second_player = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='second_player_in')

    first_player_is_X = models.BooleanField(default=True)
    first_players_turn = models.BooleanField(default=True)

    board_name = models.CharField(max_length=50)
    board_string = models.CharField(max_length=1056)

    open_game = models.BooleanField(default=False)
    game_started = models.BooleanField(default=False)
    game_ended = models.BooleanField(default=False)

    winner = models.CharField(max_length=1, null=True)
    elo_transferred = models.IntegerField(null=True)

    most_recent_move = models.DateTimeField(auto_now_add=True)

    def is_users_turn(self, user):
        if self.game_ended or not self.game_started:
            return False
        if user == self.first_player:
            self.first_players_turn
        elif user == self.second_player:
            return not self.first_players_turn
        return False
