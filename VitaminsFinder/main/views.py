from django.http import HttpResponse
from django.shortcuts import render
from .forms import SearchForm
from .models import SearchBox
#from VitaminsFinder.api.urls import create_search
#import requests


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
             print(form.cleaned_data)

    form = SearchForm()

    data = {
        'form': form
    }
    return render(request, 'main/index.html', data)


def about(request):

    return render(request, 'main/aboutUs.html')