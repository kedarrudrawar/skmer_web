from django.shortcuts import render, redirect, reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views import generic
from urllib.parse import urlencode

import os,sys,inspect
sys.path.append('/Users/KedarRudrawar/Desktop/Spring_Quarter_2019/CSE-182/skmer_web/skmer_web/')

from .forms import QueryForm, RawQueryForm
from .models import Query
from scripts.skmer_functions import parse_queryout, query
import time
BASE_DIR = '/Users/KedarRudrawar/Desktop/Spring_Quarter_2019/CSE-182/skmer_web/skmer_web/'
STATIC_DIR = BASE_DIR + 'static/'
REF_DIR_PATH = STATIC_DIR + 'ref_dir/'



class DetailView(generic.DetailView):
    model = Query
    template_name = 'queries/detail.html'
    def get_queryset(self):
        return render(Query.objects.all())


def analyze_file(request, query_id):
    query_obj = Query.objects.get(pk=query_id)
    try:
        query_file = query_obj.queryFile.path.replace(' ', '\ ')
    except KeyError:
        return render(request, 'queries/blank.html')

    else:
        print('FILE PATH', query_file)
        library_dir = STATIC_DIR + 'testlib'
        output_prefix = BASE_DIR + r'media/skmer_output/output/'
        out = query(query_file, library_dir, output_prefix, add_query_to_ref=False)
        time.sleep(5)
        print("Output file exists?", os.path.isfile(out))
        print('OUTPUT', out)
        list_of_hit_distance_pairs = parse_queryout(out)

        print(list_of_hit_distance_pairs)

        context = {
            'query': query_obj,
            'output': list_of_hit_distance_pairs
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