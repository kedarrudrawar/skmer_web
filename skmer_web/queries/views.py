from django.shortcuts import render, redirect, reverse
from django.conf import settings
from urllib.parse import urlencode
from django.http import HttpResponse
from django.template import loader
from shutil import copyfile

import os

from .forms import QueryForm, MultipleQueryForm, QueryCollectionForm
from .models import Query, Queries
from scripts.skmer_functions import *
import zipfile

STATIC_DIR = os.path.join(settings.BASE_DIR, 'static')
REF_DIR_PATH = os.path.join(STATIC_DIR, 'ref_dir')


# INPUT

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
                query_collection.query_set.create(queryFile=file)

            query_string = urlencode({'queries_id': query_collection.id})
            base_url = reverse('queries:input_multiple')
            url = '%s%s' % (base_url, query_string)

            return redirect(url)
    else:
        name_form = QueryCollectionForm()
        query_form = MultipleQueryForm()

    context = {
        'name_form': name_form,
        'query_form': query_form
    }
    print('::::::RENDERING for upload_queryfile_multiple:::::')
    return render(request, 'queries/query_multiple_create.html', context)


# ANALYSIS

def analyze_file(request, query_id):
    query_obj = Query.objects.get(pk=query_id)
    try:
        query_file = query_obj.queryFile.path.replace(' ', '\ ')
    except KeyError:
        return render(request, 'queries/blank.html')

    else:
        ########Define input/output paths
        library_dir = os.path.join(STATIC_DIR, 'large_test_lib') ## Change this for final runs
        output_prefix = os.path.join(settings.BASE_DIR, 'media/skmer_output/output')
        
        # Generate query results
        dist_file, stats_folder = query(query_file, library_dir, output_prefix)
        
        # Parse the query results into python objects
        # Set clean=True to remove intermediate files
        # Specify number of results to display (n_results=1 gives top hit only)
        list_of_hit_distance_pairs = parse_distout(dist_file, n_results=5, clean=True)
        print(list_of_hit_distance_pairs)
        
        print("Stats folder is : ", stats_folder)
        
        # Parse the statistics folder
        # Can specify # decimal places to display, and whether to clean files
        stats_dictionary = parse_statsout(stats_folder, n_decimals=5, clean=True)
        
        print(stats_dictionary)
        ######## Define filepath to where images are saved
        media_dir = settings.MEDIA_ROOT
        
        folder = os.path.join(media_dir, stats_folder)
        
        print(media_dir)
        # Generate figures for this query
        barplot_fp = plot_repeat_profile_bar(stats_dictionary, 
                                             folder, 
                                             logscale=False)
        barplot_fp = os.path.basename(barplot_fp)
#         donutplot_fp = plot_repeat_profile_donut(stats_dictionary, media_dir+stats_folder)
#         donutplot_fp = os.path.basename(donutplot_fp)
        
        
        
        context = {
            'query': query_obj,
            'output': list_of_hit_distance_pairs,
            'statistics': stats_dictionary,
            'barplot_fp': barplot_fp

        }

        return render(request, 'queries/singlequery_analysis.html', context)


def analyze_multiple(request, queries_id):
    queries_obj = Queries.objects.get(pk=queries_id)
    queries = queries_obj.query_set.all()
    files = [query.queryFile for query in queries]
    
    # Create the new library from skims
    media_dir = settings.MEDIA_ROOT

    library_dir = os.path.join(media_dir, str(queries_id))
    os.mkdir(library_dir)

    # copy CONFIG into library_dir
    CONFIG_PATH = os.path.join(settings.MEDIA_ROOT, 'queryFiles')
    CONFIG_PATH = os.path.join(CONFIG_PATH, 'CONFIG')

    copyfile(CONFIG_PATH, os.path.join(library_dir, 'CONFIG'))

    for file in files:
        filepath = file.path
        # Unzip this file into a folder, and add folder to a reference
        # library
        with zipfile.ZipFile(filepath,"r") as zip_ref:
            zip_ref.extractall(library_dir)
    
    # Generate the distance matrix from library
    dm_path = generate_distances(library_dir)
    queries_id = str(queries_id)
    dm_img_output_path = os.path.join(media_dir, queries_id+"_distance_heatmap")
    # Keep names_to_include as None to display all species
    list_of_names = plot_distance_heatmap(dm_path, dm_img_output_path,
                                              names_to_include=None)
    dm_img_output_path = os.path.basename(dm_img_output_path)

    context = {
        'files': files,
        'distance_heatmap': dm_img_output_path,
        'sci_and_common_names': list_of_names
    }

    return render(request, 'queries/multiplequery_analysis.html', context)


# LIST

def query_list(request):
    queries = Query.objects.all()
    for query in queries:
        print(str(query.queryFile))
        print(str(query.queryFile).split('/')[-1])
    file_names = [str(query.queryFile).split('/')[-1] for query in queries]
    print(file_names)
    context = {
        'queries': queries,
        'empty': len(queries) == 0,
        'file_names': file_names
    }

    return render(request, 'queries/query_list.html', context)