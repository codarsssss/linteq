from django.urls import path
from . import views


app_name = 'linteq_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('transcription', views.transcription_page, name='transcription'),
    path('result', views.result_page, name='result'),
    path('download/<path:file_path>', views.download_files, name='download')
]
