from django.shortcuts import render
from .forms import QueryForm


def query_create_view(request):
    form = QueryForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "query_create.html", context)
# Create your views here.
