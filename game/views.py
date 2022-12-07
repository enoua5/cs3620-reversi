from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from datetime import datetime

from .models import Game, BoardTemplate
from .reversi.reversi import Reversi, _Player, _Winner

def transfer_elo(playerX, playerO, winner:float):
    # winner == 0 => player X won
    # winner == 1 => player O won
    # winner == 0.5 => tie
    rX = playerX.userdata.elo_rating
    rO = playerO.userdata.elo_rating
    eX = 1 / (1 + (10 ** ( (rO-rX)/400 )))
    eO = 1 / (1 + (10 ** ( (rX-rO)/400 )))

    print("score:",winner)
    print("expected:",eO)

    print("X gets:", 16 * ((1-winner) - eX))
    print("O gets:", 16 * (winner - eO))

    playerX.userdata.elo_rating += 16 * ((1-winner) - eX)
    playerO.userdata.elo_rating += 16 * (winner - eO)
    playerX.save()
    playerO.save()

def get_game_data(game_list, user):
    role = []
    opponent = []

    for game in game_list:
        if user == game.first_player:
            opponent.append(game.second_player)
            role.append("White")
        else:
            opponent.append(game.first_player)
            role.append("Black")

    return zip(game_list, role, opponent)

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

    if not game.game_ended:

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

                game_score = 0.5
                if winner == _Winner.O:
                    game_score = 1
                    game.winner = 'o'
                elif winner == _Winner.X:
                    game_score = 0
                    game.winner = 'x'
                elif winner == _Winner.TIE:
                    game_score = 0.5
                    game.winner = 't'

                game.save()

                if game.first_player_is_X:
                    transfer_elo(game.first_player, game.second_player, game_score)
                else:
                    transfer_elo(game.second_player, game.first_player, game_score)

            except ValueError:
                print("ERROR!")

        

    return redirect('game:view_game', game_id = game_id)

def my_games(req):
    my_turn = get_game_data(Game.objects.filter(game_started=True, game_ended=False).filter(Q(first_players_turn=True, first_player=req.user) | Q(first_players_turn=False, second_player=req.user)), req.user)
    opp_turn = get_game_data(Game.objects.filter(game_started=True, game_ended=False).filter(Q(first_players_turn=True, second_player=req.user) | Q(first_players_turn=False, first_player=req.user)), req.user)
    finshed = get_game_data(Game.objects.filter(game_ended=True), req.user)


    ctx = {
        'my_turn': my_turn,
        'opp_turn': opp_turn,
        'finished': finshed,
    }

    return render(req, 'game/my_games.html', ctx)

