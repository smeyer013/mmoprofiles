"""MMOP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views as main_views
from account import views as accounts_views
from profiles import views as profile_views
from search import views as search_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.home),
    path('join/', accounts_views.join),
    path('login/', accounts_views.usrlogin),
    path('logout/', accounts_views.usrlogout),
    path('profile/', profile_views.profile),
    path('profile/game/', profile_views.addgame),
    path('profile/build/<int:id>/', profile_views.addbuild),
    path('profile/edit/game/<int:id>/', profile_views.editgame),
    path('profile/edit/build/<int:id>/', profile_views.editbuild),
    path('profile/game/', profile_views.addgame),
    path('search/', search_views.search),
    path('gamesearch/', search_views.gamesearch),
    path('playersearch/', search_views.playersearch),
]
