from django.shortcuts import render, redirect
from .trascription_logic import transcript_file
from .forms import FilePostForm, ConsultationForm
from django.contrib import messages

# Create your views here.


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

            return render(request, 'linteq_app/index-sys-UI.html', context={
                'result': transcript_file(form_object['file'],
                                          form_object['file_name'],
                                          str(form_object['file']).split('.')[-1])})
        else:
            form = FilePostForm()

    context = {
        'title': 'Linteq'
    }

    return render(request, 'linteq_app/index-sys-UI.html', context=context)
