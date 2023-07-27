import os
from datetime import datetime
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect
from .trascription_logic import transcript_file
from .forms import FilePostForm, ConsultationForm
from django.contrib import messages
from django.conf import settings


def download_files(request, file_path):
    file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_full_path):
        return FileResponse(open(file_full_path, 'rb'))
    raise Http404('Такого файла не существует :(')


def handle_form(request, form_class):
    form = form_class(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Мы получили ваш запрос!')
        return True
    else:
        form = form_class()
        return False


def index(request):
    if request.method == 'POST':
        if handle_form(request, ConsultationForm):
            return redirect('/')

    context = {
        'title': 'Linteq'
    }

    return render(request, 'linteq_app/index.html', context=context)


def transcription_page(request):
    if request.method == "POST" and request.FILES:
        form = FilePostForm(request.POST, request.FILES)
        if form.is_valid():
            form_object = form.cleaned_data
            request.session['result'] = transcript_file(form_object['file'],
                                          form_object['file_name'],
                                          str(form_object['file']).split('.')[-1],
                                          form_object['model_type'],
                                          datetime.now(),
                                          form_object['original_language'],
                                          form_object['translate_language'],
                                          form_object['translate_checkBox'])
            return redirect('linteq_app:result')
        else:
            form = FilePostForm()

    context = {
        'title': 'Linteq'
    }

    return render(request, 'linteq_app/index-sys-UI.html', context=context)


def result_page(request):
    context = {
        'title': 'Linteq',
        'result': request.session.get('result')
    }
    return render(request, 'linteq_app/result.html', context=context)
