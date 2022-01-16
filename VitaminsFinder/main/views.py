
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .parsers import iherb
from .forms import SearchForm
from django.db import connection
from .models import SearchBox
from django.http import StreamingHttpResponse
import wsgiref
from wsgiref.util import FileWrapper
import mimetypes
import os



def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            searchzapros = (form.cleaned_data['search_text'])
            min_price = (form.cleaned_data['min_price'])
            max_price = (form.cleaned_data['max_price'])
            iherb.main(searchzapros, min_price, max_price)






    form = SearchForm()

    data = {
        'form': form
    }
    return render(request, 'main/index.html', data)


def about(request):

    return render(request, 'main/aboutUs.html')


def downloadfile(req):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'test.xlsx'
    filepath = base_dir + '/Files/' + filename
    thefile = filepath
    filename = os.path.basename(thefile)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'), chunk_size), content_type=mimetypes.guess_type(thefile)[0])
    response['Content-Length'] = os.path.getsize(thefile)
    response['Content-Disposition'] = "Attachment;filename=%s" % filename
    return response