from django import forms 
from main.models import Game, GameInstance, SpecInstance, GuildInstance 

class GameForm(forms.ModelForm):
    level = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '24'}))
    class Meta(): 
        model = GameInstance
        fields = ('game', 'level', 'active')
        labels = {
            'spec': ('Class')
        }

class GameEditForm(forms.ModelForm):
    level = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '24'}))
    class Meta(): 
        model = GameInstance
        fields = ('level', 'active')
        labels = {
            'spec': ('Class')
        }

class SpecForm(forms.ModelForm):
    game = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '24','readonly':'readonly'}))
    role = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '24'}))
    spec = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '24'}))
    class Meta(): 
        model = SpecInstance 
        fields = ('role', 'spec')
        labels = {
            'spec': ('Class')
        }

class SpecEditForm(forms.ModelForm):
    game = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '24','readonly':'readonly'}))
    role = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '24'}))
    spec = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '24'}))
    class Meta(): 
        model = SpecInstance 
        fields = ('role', 'spec')
        labels = {
            'spec': ('Class')
        }