from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required
def index(req):
    top_players = User.objects.all().order_by('userdata__elo_rating')[:5]

    ctx = {
        'top_players': top_players
    }

    return render(req, 'base/index.html', ctx)
