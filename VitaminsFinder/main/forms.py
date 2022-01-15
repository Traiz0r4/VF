from django.forms import ModelForm, TextInput, NumberInput
from .models import SearchBox


class SearchForm(ModelForm):
    class Meta:
        model = SearchBox
        fields = ['search_text', 'min_price', 'max_price']

        widgets = {
            'search_text': TextInput(attrs={
                'class': 'search-box',
                'placeholder': 'Введите для поиска'}),

            'min_price': NumberInput(attrs={
            'class': 'range-min price-range>input',
            'placeholder': 'min',
            }),

            'max_price': NumberInput(attrs={
                    'class': 'range-max price-range>input',
                    'placeholder': 'max',
            })
        }