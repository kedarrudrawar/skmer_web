from django.shortcuts import render, redirect, reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views import generic
from urllib.parse import urlencode

from .forms import QueryForm, RawQueryForm
from .models import Query
from ..scripts.skmer_functions import parse_queryout, query

import os


REF_DIR_PATH = '/Users/KedarRudrawar/Desktop/Spring Quarter 2019/CSE-182/skmer_web/skmer_web/static/ref_dir/'



class DetailView(generic.DetailView):
    model = Query
    template_name = 'queries/detail.html'
    def get_queryset(self):
        return render(Query.objects.all())


def analyze_file(request, query_id):
    query_obj = Query.objects.get(pk=query_id)
    try:
        queryFile = query_obj.queryFile
    except KeyError:
        return render(request, 'queries/blank.html')

    else:
        query_file = "Skmer_old/data/qry.fastq"
        library_dir = "Skmer_old/data/testlib"
        output_prefix = "Skmer_old/data/PYTHONTEST11"
        out = query(query_file, library_dir, output_prefix, add_query_to_ref=False)
        list_of_hit_distance_pairs = parse_queryout(out)

        context = {
            'query': query
        }

        return render(request, 'queries/analysis.html', context)


# def query_create_view(request):
#     form = RawQueryForm()
#     if request.method == 'POST':
#         form = RawQueryForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             Query.objects.create(**form.cleaned_data)
#         else:
#             print(form.errors)
#
#     context = {
#         'form': form
#     }
#     return render(request, 'queries/query_create.html', context)


# def upload_file(request):
#     if request.method == 'POST':
#         file = request.FILES.get('Query file')
#         storage = FileSystemStorage()
#         storage.save(file.name, file)
#         file_path = '\"' + os.path.join(settings.MEDIA_ROOT, file.name) + '\"'
#         print(file_path)
#
#         command = 'python3 scripts/test.py -f {}'.format(file_path)
#         output = os.popen(command).read()
#         print(output)
#
#     return render(request, 'queries/query_create.html')


def query_list(request):
    queries = Query.objects.all()
    lengths = [q.queryFile.size for q in queries]
    print(queries)
    print(lengths)
    context = {
        'queries': queries,
        'sizes': lengths
    }

    return render(request, 'queries/query_list.html', context)


def upload_queryfile(request):
    if request.method == 'POST':
        form = QueryForm(request.POST, request.FILES)
        if form.is_valid():
            q = form.save()
            query_string = urlencode({'query_id': q.id})

            base_url = reverse('queries:query_list')
            url = '%s%s' % (base_url, query_string)
            return redirect(url)
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