from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from main.models import Game, GuildInstance
from search.forms import SearchForm

@login_required(login_url="/login/")
def search(request):
    context = {}
    
    return render(request,'search/search.html', context)

def search(request):
    if (request.method == "POST"):
        if ("search" in request.POST):
            search_form = SearchForm(request.POST)
            if (search_form.is_valid()):
                # default is that all items are valid in the search
                results = {'games':Game.objects.all(),'players':get_user_model().objects.all(),'guilds':GuildInstance.objects.all()}
                context = {
                    "search_form": SearchForm(),
                    "search_results": results,
                    "search_type": 0,
                    "searched": True,
                }
                criteria = search_form.cleaned_data["criteria"]
                context["search_criteria"] = [criteria]
                try:
                    results['games'] = Game.objects.filter(name__icontains=criteria)
                    results['players'] = get_user_model().objects.filter(name__icontains=criteria)
                    context["search_type"] = 0
                    context["search_results"] = results
                except Game.DoesNotExist:
                    context["search_results"] = []
                return render(request, 'search/search.html', context)
            else:
                context = {
                    "form_data": search_form
                }
                return render(request, 'search/search.html', context)
        else:
            return redirect("/search/")
    else:
        context = {
            "search_form": SearchForm(),
            "search_results": [],
            "searched": False,
        }
        return render(request, 'search/search.html', context)

def gamesearch(request):
    if (request.method == "POST"):
        if ("search" in request.POST):
            search_form = SearchForm(request.POST)
            if (search_form.is_valid()):
                # default is that all games are valid in the search
                results = {'games':Game.objects.all()}
                context = {
                    "search_form": SearchForm(),
                    "search_results": results,
                    "search_type": 0,
                    "searched": True,
                }
                criteria = search_form.cleaned_data["criteria"]
                context["search_criteria"] = [criteria]
                try:
                    results['games'] = Game.objects.filter(name__icontains=criteria)
                    context["search_type"] = 1
                    context["search_results"] = results
                except Game.DoesNotExist:
                    context["search_results"] = []
                print (context['search_type'])
                return render(request, 'search/search.html', context)
            else:
                context = {
                    "form_data": search_form
                }
                return render(request, 'search/search.html', context)
        else:
            return redirect("/gamesearch/")
    else:
        context = {
            "search_form": SearchForm(),
            "search_results": [],
            "searched": False,
        }
        return render(request, 'search/search.html', context)

def playersearch(request):
    if (request.method == "POST"):
        if ("search" in request.POST):
            search_form = SearchForm(request.POST)
            if (search_form.is_valid()):
                # default is that all games are valid in the search
                results = {'players':get_user_model().objects.all()}
                context = {
                    "search_form": SearchForm(),
                    "search_results": results,
                    "search_type": 0,
                    "searched": True,
                }
                criteria = search_form.cleaned_data["criteria"]
                context["search_criteria"] = [criteria]
                try:
                    results['players'] = get_user_model().objects.filter(name__icontains=criteria)
                    context["search_type"] = 2
                    context["search_results"] = results
                except Game.DoesNotExist:
                    context["search_results"] = []
                return render(request, 'search/search.html', context)
            else:
                context = {
                    "form_data": search_form
                }
                return render(request, 'search/search.html', context)
        else:
            return redirect("/playersearch/")
    else:
        context = {
            "search_form": SearchForm(),
            "search_results": [],
            "searched": False,
        }
        return render(request, 'search/search.html', context)