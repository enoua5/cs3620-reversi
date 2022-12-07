from django.urls import path
from . import views

app_name = "base"
urlpatterns = [
    path('', views.index, name="index"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('edit-profile', views.edit_profile, name="edit_profile"),

    path('users/', views.list_all_users, name="user_list"),
    path('users/search/<int:min_elo>/<int:max_elo>/<str:username>', views.list_all_users_search, name="search_users"),
]
