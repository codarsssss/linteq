from django.shortcuts import render
from .trascription_logic import transcription_video

# Create your views here.


def index(request):

    if request.method == 'POST' and request.FILES:
        file = request.FILES['file_input']
        file_extension = str(file).split('.')[-1]

        # Проверка формата файла.
        context = {
        'title': 'Linteq',
        'result': transcription_video(file, file_extension)
        }
        return render(request, 'linteq_app/index.html', context=context)


    context = {
        'title': 'Linteq'
    }

    return render(request, 'linteq_app/index.html', context=context)
