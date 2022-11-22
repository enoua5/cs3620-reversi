from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from django.core.paginator import Paginator

from .models import Game, BoardTemplate

# Create your views here.

def open_games_list(req, page):
    games = Game.objects.filter(open_game = True, game_started = False)

    paginator = Paginator(games, 30)
    games = paginator.get_page(page)

    ctx = {
        'page': page,
        'games': games
    }

    return render(req, 'game/open_game_list.html', ctx)

def new_game(req):

    if req.method == 'POST':
        player_is_X = req.POST.get("play_as") == "white"
        player_goes_first = player_is_X
        board_id = req.POST.get('board')
        board = BoardTemplate.objects.get(id=board_id)


        game = Game(
            first_player = req.user,
            first_player_is_X = player_is_X,
            first_players_turn = player_goes_first,
            open_game = True,
            board_string = board.board_string,
            board_name = board.name
        )
        
        game.save()

        return redirect('game:view_game', game_id = game.id)

    boards = BoardTemplate.objects.all()

    ctx = {
        'boards': boards
    }

    return render(req, 'game/create_game.html', ctx)

def view_game(req, game_id):
    game = Game.objects.get(id=game_id)
    turn = game.first_player if game.first_players_turn else game.second_player

    ctx = {
        'game': game,
        'turn': turn
    }

    return render(req, 'game/game.html', ctx)
