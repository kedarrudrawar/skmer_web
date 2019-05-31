from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .forms import QueryForm, RawQueryForm
from .models import Query

import os


def query_create_view(request):
    form = RawQueryForm()
    if request.method == 'POST':
        form = RawQueryForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Query.objects.create(**form.cleaned_data)
        else:
            print(form.errors)

    context = {
        'form': form
    }
    return render(request, 'queries/query_create.html', context)


def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('Query file')
        storage = FileSystemStorage()
        storage.save(file.name, file)
        file_path = '\"' + os.path.join(settings.MEDIA_ROOT, file.name) + '\"'
        print(file_path)

        command = 'python3 scripts/test.py -f {}'.format(file_path)
        output = os.popen(command).read()
        print(output)

    return render(request, 'queries/query_create.html')


def query_list(request):
    queries = Query.objects.all()

    # lengths = [q.queryFile.length for q in queries]

    context = {
        'queries': queries
        # 'length': lengths
    }

    return render(request, 'queries/query_list.html', context)


def upload_queryfile(request):
    if request.method == 'POST':
        form = QueryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('query_list')
    else:
        form = QueryForm()

    context = {
        'form': form
    }

    return render(request, 'queries/query_create.html', context)



# def query_create_view(request):
#     if request.method == 'POST':
#         title = request.POST.get('Title')
#         print(title)
#
#     context = {}
#     # form = QueryForm(request.POST or None)
#     # if form.is_valid():
#     #     form.save()
#     #     form = QueryForm()
#     # context = {
#     #     'form': form
#     # }
#     return render(request, "queries/query_create.html", context)


# def query_create_view(request):
#     form = QueryForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         form = QueryForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'queries/query_create.html', context)