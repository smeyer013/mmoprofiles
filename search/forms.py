from django import forms
from search.models import Search

class SearchForm(forms.ModelForm):
    criteria = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '48'}))
    class Meta():
        model = Search
        fields = ('criteria',)
        labels = {
            'criteria': ('Search')
        }