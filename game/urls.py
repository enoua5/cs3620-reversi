from django.urls import path
from . import views

app_name = "game"
urlpatterns = [
    path('open_games/<int:page>', views.open_games_list, name="open_games"),
    path('new_open/', views.new_game, name="new_open_game"),
    path('play/<int:game_id>', views.view_game, name="view_game"),
    path('play/<int:game_id>/<int:row>/<int:col>', views.make_move, name="make_move"),
    path('join/<int:game_id>', views.join_game, name="join_game"),
    path('my_games', views.my_games, name="my_games"),
]
