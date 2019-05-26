from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import RefFile

# Create your views here.
def home_view(request, *args, **kwargs):
    my_context = {
        "my_text": "This is my text",
        "my_number": 123,
        "my_list": [1,2,3,4]
    }
    return render(request, "home.html", my_context)


def detail_view(request, *args, **kwargs):
    r = RefFile.objects.get(id=1)
    context = {
        'RefFile': r
    }
    print(context)
    return render(request, "reference/detail.html", context)