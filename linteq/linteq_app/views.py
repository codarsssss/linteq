from django.shortcuts import render
from .trascription_logic import choice_audio_or_video_format

# Create your views here.


def index(request):

    if request.method == 'POST' and request.FILES:
        file = request.FILES['file_input']

        # Проверка формата файла.
        context = {
        'title': 'Linteq',
        'result': choice_audio_or_video_format(file)
        }
        return render(request, 'linteq_app/index.html', context=context)


    context = {
        'title': 'Linteq'
    }

    return render(request, 'linteq_app/index.html', context=context)
