from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from game.models import Game

# Create your views here.

@login_required
def index(req):
    top_players = User.objects.all().order_by('-userdata__elo_rating')[:5]

    latest_games = Game.objects.filter(Q(first_player=req.user) | Q(second_player=req.user)).order_by('-most_recent_move')[:5]

    player_role = []
    player_opp = []

    for game in latest_games:
        player_role.append("White" if game.first_player_is_X ^ (game.second_player == req.user) else "Black")
        player_opp.append(game.first_player if game.second_player == req.user else game.second_player)

    latest_games = list(zip(latest_games, player_role, player_opp))

    ctx = {
        'top_players': top_players,
        'latest_games': latest_games,
    }

    return render(req, 'base/index.html', ctx)
