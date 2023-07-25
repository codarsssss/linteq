from django.urls import path
from . import views


app_name = 'linteq_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('transcription', views.transcription_page, name='transcription')
]
