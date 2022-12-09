from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from game.models import Game, Challenge, BoardTemplate

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

@login_required
def profile(req, username):
    user = User.objects.get(username=username)

    ctx = {
        'user': user,
    }

    return render(req, 'base/profile.html', ctx) 

@login_required
def edit_profile(req):
    if req.POST:
        bio = req.POST.get('bio')
        open_challenge = req.POST.get('open-to-challenge') == 'on'

        req.user.userdata.bio_text = bio
        req.user.userdata.open_for_challenge = open_challenge

        req.user.save()

        return redirect('base:profile', username=req.user.username)


    return render(req, 'base/edit_profile.html')

def handle_search(req):
    if req.POST:
        username = req.POST.get("username")
        if username == "":
            username = "*"
        minelo = int(req.POST.get("minelo"))
        maxelo = int(req.POST.get("maxelo"))

        return redirect('base:search_users', min_elo=minelo, max_elo=maxelo, username=username)
    return None

@login_required
def list_all_users(req):

    search = handle_search(req)
    if search is not None:
        return search

    users = User.objects.all().order_by('-userdata__elo_rating')

    ctx = {
        'users': users
    }

    return render(req, 'base/user_list.html', ctx)

@login_required
def list_all_users_search(req, min_elo:int, max_elo:int, username:str):

    search = handle_search(req)
    if search is not None:
        return search

    users = User.objects.filter(userdata__elo_rating__gte=min_elo, userdata__elo_rating__lte=max_elo)
    if username != "*":
        users = users.filter(username__contains=username)
    users = users.order_by('-userdata__elo_rating')

    ctx = {
        'users': users
    }

    return render(req, 'base/user_list.html', ctx)

@login_required
def challenges(req):
    incoming = Challenge.objects.filter(challenged = req.user)
    sent = Challenge.objects.filter(challenger = req.user)

    ctx = {
        'incoming': incoming,
        'sent': sent,
    }


    return render(req, 'base/challenges.html', ctx)

@login_required
def accept_challenge(req, id):
    challenge_exists = True
    try:
        challenge = Challenge.objects.get(id=id)
    except:
        messages.warning(req, "Sorry, that challenge does not exist")
        challenge_exists = False

    if challenge_exists:
        if challenge.challenged == req.user:
            game = Game(
                first_player = challenge.challenger,
                second_player = challenge.challenged,
                first_player_is_X = challenge.challenger_is_X,
                first_players_turn = challenge.challenger_is_X,
                open_game = False,
                board_string = challenge.board_id.board_string,
                board_name = challenge.board_id.name,
                game_started = True
            )

            game.save()
            challenge.delete()

            return redirect('game:view_game', game_id = game.id)


        else:
            messages.warning(req, "Sorry, that challenge isn't for you")
    
    # if we fell through and didn't make it to the create game branch
    return redirect('base:challenges')


@login_required
def delete_challenge(req, id):
    challenge_exists = True
    try:
        challenge = Challenge.objects.get(id=id)
    except:
        messages.warning(req, "Sorry, that challenge does not exist")
        challenge_exists = False

    
    if challenge_exists:
        if challenge.challenger == req.user or challenge.challenged == req.user:
            challenge.delete()
            messages.success(req, "Challenge deleted")
        else:
            messages.warning(req, "You do not have permission to delete that challenge")

    return redirect('base:challenges')
