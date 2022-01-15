from django.http import HttpResponse
from django.shortcuts import render
from .parsers import iherb
from .forms import SearchForm
from .models import SearchBox



def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            searchzapros = (form.cleaned_data['search'])
            iherb.main(searchzapros)




    form = SearchForm()

    data = {
        'form': form
    }
    return render(request, 'main/index.html', data)


def about(request):

    return render(request, 'main/aboutUs.html')