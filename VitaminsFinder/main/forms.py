from django.forms import ModelForm, TextInput
from .models import SearchBox


class SearchForm(ModelForm):
    class Meta:
        model = SearchBox
        fields = ['search']

        widgets = {
            'search': TextInput(attrs={
                'class': 'search-box',
                'placeholder': 'Введите для поиска'
            })
        }