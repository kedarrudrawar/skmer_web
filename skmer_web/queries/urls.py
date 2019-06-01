from django.urls import path, re_path
from . import views

app_name = 'queries'
urlpatterns = [
    path('analyze/', views.upload_queryfile, name='input'),
    path('query_list/', views.query_list, name='query_list'),
    path(r'query_list/query_id=<int:query_id>', views.analyze_file, name='analyze')
]