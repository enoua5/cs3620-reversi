from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from game.models import Game

def get_player_games(user, count=-1):
    latest_games = Game.objects.filter(Q(first_player=user) | Q(second_player=user)).order_by('-most_recent_move')

    if count > 0:
        latest_games = latest_games[:count]

    player_role = []
    player_opp = []

    for game in latest_games:
        player_role.append("White" if game.first_player_is_X ^ (game.second_player == user) else "Black")
        player_opp.append(game.first_player if game.second_player == user else game.second_player)

    return list(zip(latest_games, player_role, player_opp))


# Create your views here.

@login_required
def index(req):
    top_players = User.objects.all().order_by('-userdata__elo_rating')[:5]

    latest_games = get_player_games(req.user, 5)

    ctx = {
        'top_players': top_players,
        'latest_games': latest_games,
    }

    return render(req, 'base/index.html', ctx)
