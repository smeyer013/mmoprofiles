from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from main.models import Game, GameInstance, SpecInstance, GuildInstance
from profiles.forms import GameForm, GameEditForm, SpecForm, SpecEditForm

@login_required(login_url="/login/")
def profile(request):
    if (request.method == "GET" and "deletegame" in request.GET):
        id = request.GET["deletegame"]
        game_name = GameInstance.objects.get(id=id).game
        game_active = GameInstance.objects.get(id=id).active

        # Remove the player from the game's player count
        # if the player had marked the game as active.
        if (game_active):
            game_name.players = game_name.players - 1
            game_name.save()

        # Deleting a game also deletes any builds the player had attached to it.
        SpecInstance.objects.filter(user=request.user,game=game_name).delete()
        GameInstance.objects.filter(id=id).delete()
        return redirect("/profile")
    
    if (request.method == "GET" and "deletebuild" in request.GET):
        id = request.GET["deletebuild"]
        SpecInstance.objects.filter(id=id).delete()
        return redirect("/profile")
    
    # Player profiles are where they can change their interests,
    # stats, groups, and anything else.

    # Get user's game data, if any exists.
    try:
        user_games = GameInstance.objects.filter(user=request.user)
    except GameInstance.DoesNotExist:
        user_games = []

    # Get user's spec data, if any exists.
    try:
        user_specs = SpecInstance.objects.filter(user=request.user)
    except SpecInstance.DoesNotExist:
        user_specs = []
    
    # Get user's guild data, if any exists.
    try:
        user_guilds = GuildInstance.objects.filter(user=request.user)
    except GuildInstance.DoesNotExist:
        user_guilds = []

    # Now make use of the data to separate all of the player's
    # data by the game it pertains to.
    guilds = {}

    context = {
        "games": user_games,
        "specs": user_specs,
        "guilds": guilds,
    }
    
    return render(request,'profiles/profile.html', context)

@login_required(login_url='/login/')
def addgame(request):
    if (request.method == "POST"):
        if ("add" in request.POST):
            game_form = GameForm(request.POST)
            if (game_form.is_valid()):
                game = game_form.cleaned_data["game"]
                level = game_form.cleaned_data["level"]
                active = game_form.cleaned_data["active"]
                user = get_user_model().objects.get(id=request.user.id)

                # The game is new to the player's list.
                if (not GameInstance.objects.filter(user=user, game=game) and active):
                    game.players = game.players + 1
                    game.save()
                # The player had the game in their list but now marked it as inactive.
                elif (GameInstance.objects.filter(user=user, game=game, active=True) and not active):
                    game.players = game.players - 1
                    game.save()
                # The player had the game in their list but now marked it as active.
                elif (GameInstance.objects.filter(user=user, game=game, active=False) and active):
                    game.players = game.players + 1
                    game.save()

                # Now add the game to player's page, removing it if it was already there.
                GameInstance.objects.filter(user=user, game=game).delete()
                GameInstance(user=user, game=game, level=level, active=active).save()
                return redirect("/profile/")
            else:
                context = {
                    "form_data": game_form
                }
                return render(request, 'profiles/addgame.html', context)
        else:
            # Cancel
            return redirect("/profile")
    else:
        context = {
            "form_data": GameForm()
        }
        return render(request, 'profiles/addgame.html', context)

@login_required(login_url='/login/')
def editgame(request, id):
    if (request.method == "GET"):
        # Load Form with current model data.
        gameEntry = GameInstance.objects.get(id=id)
        form = GameEditForm(instance=gameEntry)
        context = {"form_data": form}
        return render(request, 'profiles/editgame.html', context)
    elif (request.method == "POST"):
        # Process form submission
        if ("editgame" in request.POST):
            form = GameEditForm(request.POST)
            if (form.is_valid()):
                gameEntry = form.save(commit=False)
                gameEntry.user = request.user
                gameEntry.id = id
                gameEntry.level = GameInstance.objects.get(id=id).level
                gameEntry.active = GameInstance.objects.get(id=id).active
                gameEntry.save()
                return redirect("/profile/")
            else:
                context = {
                    "form_data": form
                }
                return render(request, 'profiles/editgame.html', context)
        else:
            # Cancel
            return redirect("/profile/")

@login_required(login_url='/login/')
def addbuild(request, id):
    if (request.method == "POST"):
        if ("addbuild" in request.POST):
            spec_form = SpecForm(request.POST)
            if (spec_form.is_valid()):
                game = GameInstance.objects.get(id=id).game
                role = spec_form.cleaned_data["role"]
                spec = spec_form.cleaned_data["spec"]
                user = get_user_model().objects.get(id=request.user.id)
                SpecInstance(user=user, game=game, role=role, spec=spec).save()
                return redirect("/profile/")
            else:
                context = {
                    "form_data": spec_form
                }
                return render(request, 'profiles/addbuild.html', context)
        else:
            # Cancel
            return redirect("/profile")
    else:
        context = {
            "form_data": SpecForm({'game':GameInstance.objects.get(id=id).game})
        }
        return render(request, 'profiles/addbuild.html', context)

@login_required(login_url='/login/')
def editbuild(request, id):
    if (request.method == "GET"):
        # Load Form with current model data.
        specEntry = SpecInstance.objects.get(id=id)
        form = SpecEditForm({'game':SpecInstance.objects.get(id=id).game,
            'role':SpecInstance.objects.get(id=id).role,
            'spec':SpecInstance.objects.get(id=id).spec})
        context = {"form_data": form}
        return render(request, 'profiles/editbuild.html', context)
    elif (request.method == "POST"):
        # Process form submission
        if ("editbuild" in request.POST):
            form = SpecEditForm(request.POST)
            if (form.is_valid()):
                specEntry = form.save(commit=False)
                specEntry.user = request.user
                specEntry.id = id
                specEntry.game = SpecInstance.objects.get(id=id).game
                specEntry.role = SpecInstance.objects.get(id=id).role
                specEntry.spec = SpecInstance.objects.get(id=id).spec
                specEntry.save()
                return redirect("/profile/")
            else:
                context = {
                    "form_data": form
                }
                return render(request, 'profiles/editbuild.html', context)
        else:
            # Cancel
            return redirect("/profile/")