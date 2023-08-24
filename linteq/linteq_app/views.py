import asyncio
import os
from datetime import datetime
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect
from .trascription_logic import transcript_file
from .forms import FilePostForm, ConsultationForm, FilePostEditingForm
from django.contrib import messages
from django.conf import settings
from .notification_bot import send_telegram_message
from .post_editing_logic import read_table_file

def download_files(request, file_path):
    file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_full_path):
        return FileResponse(open(file_full_path, 'rb'))
    raise Http404('Такого файла не существует :(')


def from_url_choice(request, endpoint:str):
    
    if settings.ALLOWED_HOSTS:
        request.session['from_url'] = f'{settings.ALLOWED_HOSTS[0]}/{endpoint}'
    else:
        request.session['from_url'] = f'http://127.0.0.1:8000/{endpoint}'
        
        
def handle_form(request, form_class):
    form = form_class(request.POST)
    if form.is_valid():
        form.save()
        asyncio.run(send_telegram_message(
            f'Имя: {form.instance.name}\nПочта: {form.instance.email}\n'
            f'Тема: {form.instance.subject}'))
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
                                          datetime.now(),
                                          form_object['translate_language'],
                                          translate_checkBox=form_object['translate_checkBox'])
        
            from_url_choice(request, 'transcription')
        
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
        'result': request.session.get('result'),
        'from_url': request.session.get('from_url')
    }
    return render(request, 'linteq_app/result.html', context=context)


def post_editing_page(request):
    if request.method == "POST" and request.FILES:
        form = FilePostEditingForm(request.POST, request.FILES)
        if form.is_valid():
            form_object = form.cleaned_data
            request.session['result'] = read_table_file(form_object['file'])
            
            from_url_choice(request, 'post_editing')
            
            return redirect('linteq_app:result')
        else:
            form = FilePostEditingForm()

    context = {
        'title': 'Постредактирование машинного перевода'
    }

    return render(request, 'linteq_app/post-editing.html', context=context)