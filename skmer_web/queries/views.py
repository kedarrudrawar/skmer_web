from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.conf import settings
from urllib.parse import urlencode

import os,sys,inspect
sys.path.append(settings.BASE_DIR)

from .forms import QueryForm, MultipleQueryForm, QueryCollectionForm
from .models import Query, Queries
from scripts.skmer_functions import parse_queryout, query

STATIC_DIR = os.path.join(settings.BASE_DIR, 'static')
REF_DIR_PATH = os.path.join(STATIC_DIR, 'ref_dir')


def analyze_file(request, query_id):
    query_obj = Query.objects.get(pk=query_id)
    try:
        query_file = query_obj.queryFile.path.replace(' ', '\ ')
    except KeyError:
        return render(request, 'queries/blank.html')

    else:
        library_dir = os.path.join(STATIC_DIR, 'testlib')
        output_prefix = os.path.join(settings.BASE_DIR, 'media/skmer_output/output')
        out = query(query_file, library_dir, output_prefix, add_query_to_ref=False)
        list_of_hit_distance_pairs = parse_queryout(out)

        print(list_of_hit_distance_pairs)

        context = {
            'query': query_obj,
            'output': list_of_hit_distance_pairs
        }

        return render(request, 'queries/singlequery_analysis.html', context)


def analyze_multiple(request, queries_id):
    queries_obj = Queries.objects.get(pk=queries_id)
    queries = queries_obj.query_set.all()
    files = [query.queryFile for query in queries]
    context = {
        'files': files
    }
    return render(request, 'queries/multiplequery_analysis.html', context)



def query_list(request):
    queries = Query.objects.all()
    lengths = [q.queryFile.size for q in queries]
    print(queries)
    context = {
        'queries': queries,
        'empty': len(queries) == 0
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


def upload_queryfile_multiple(request):
    if request.method == 'POST':
        name_form = QueryCollectionForm(request.POST)
        query_form = MultipleQueryForm(request.POST, request.FILES)

        files = request.FILES.getlist('queryFile')

        if name_form.is_valid() and query_form.is_valid():
            query_collection = name_form.save()
            for file in files:
                print(file)
                query_collection.query_set.create(queryFile=file)

            print(query_collection.query_set.all())
            query_string = urlencode({'queries_id': query_collection.id})

            base_url = reverse('queries:input_multiple')
            url = '%s%s' % (base_url, query_string)
            return redirect(url)
    else:
        name_form = QueryCollectionForm()
        query_form = MultipleQueryForm()

    context = {
        'name_form': name_form,
        'query_form': query_form,
    }

    return render(request, 'queries/query_multiple_create.html', context)





# class DetailView(generic.DetailView):
#     model = Query
#     template_name = 'queries/detail.html'
#     def get_queryset(self):
#         return render(Query.objects.all())




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