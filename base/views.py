from django.shortcuts import render, redirect
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

