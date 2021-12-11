from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from account.forms import RegisterForm, LoginForm
from main.models import Game, GameInstance
@login_required(login_url="/login/")
def home(request):
    # Popular games are defined by how many users
    # on the site have set it as one of their
    # active games. Five games will be listed,
    # each with a couple statistics about it.

    # Define default games if none exist
    if (not Game.objects.all()):
        Game.objects.create(name="Elder Scrolls Online")
        Game.objects.create(name="New World")
        Game.objects.create(name="Destiny 2")
    
    players = {}
    popular_names = []
    popular_nums = {}
    try:
        for item in Game.objects.all():
            players[item.name] = item.players
    except Game.DoesNotExist:
        players = {'none':0}

    # Top 5 most popular games by count of **ACTIVE** players
    for item in range(0,5):
        max_players = max(players, key=players.get)
        max_value = max(players.values())
        if max_value > 0:
            popular_names.append(max_players)
            popular_nums[max_players] = max_value
        players[max_players] = 0 # so it doesn't get picked twice
    
    context = {
        "popular_games": popular_names,
        "player_counts": popular_nums
    }
    
    return render(request,'main/home.html', context)