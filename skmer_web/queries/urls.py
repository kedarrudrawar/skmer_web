from django.urls import path
from . import views

app_name = 'queries'
urlpatterns = [
    path('analyze/single/', views.upload_queryfile, name='input_single'),
    path('analyze/multiple/', views.upload_queryfile_multiple, name='input_multiple'),
    path('query_list/', views.query_list, name='query_list'),
    path(r'query_list/query_id=<int:query_id>', views.analyze_file, name='analyze'),
    path(r'analyze/multiple/queries_id=<int:queries_id>', views.analyze_multiple, name='analyze_queries')
]