from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages

from datetime import datetime

from .models import Game, BoardTemplate
from .reversi.reversi import Reversi, _Player, _Winner

# Create your views here.

def open_games_list(req, page):
    games = Game.objects.filter(open_game = True, game_started = False).exclude(first_player = req.user)

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

def join_game(req, game_id):
    game = Game.objects.get(id=game_id)

    if game.game_started or game.first_player == req.user:
        prev_page = req.META.get("HTTP_REFERER") or "/"
        messages.warning(req, "Could not join that game")
        return redirect(prev_page)

    game.second_player = req.user
    game.game_started = True

    game.save()

    return redirect('game:view_game', game_id = game.id)
        
def make_move(req, game_id, row, col):
    game = Game.objects.get(id=game_id)

    player_to_move = game.first_player if game.first_players_turn else game.second_player

    if req.user == player_to_move:
        turn = _Player.O if game.first_player_is_X ^ game.first_players_turn else _Player.X
        
        reversi = Reversi.from_board_string(game.board_string, turn)

        try:
            reversi.play_move(row, col)

            game.first_players_turn = (reversi.turn == _Player.O) ^ game.first_player_is_X
            game.most_recent_move = datetime.now()
            game.board_string = str(reversi)

            winner = reversi.get_winner()
            ongoing = winner == _Winner.ONGOING
            if not ongoing:
                game.game_ended = True

            if winner == _Winner.O:
                game.winner = 'o'
            elif winner == _Winner.X:
                game.winner = 'x'
            elif winner == _Winner.TIE:
                game.winner = 't'

            game.save()

        except ValueError:
            print("ERROR!")

        

    return redirect('game:view_game', game_id = game_id)

def my_games(req):
    return render(req, 'game/my_games.html')

