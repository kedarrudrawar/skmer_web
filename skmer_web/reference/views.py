from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.
def home_view(request, *args, **kwargs):
    print(request)
    print(request.user)
    # return HttpResponse("<h1> Home page. </h1>") 
    return render(request, "home.html", {})
