from django.shortcuts import render
from .trascription_logic import transcription_audio

# Create your views here.


def index(request):
    context = {
        'title': 'Linteq'
    }

    if request.method == 'POST' and request.FILES:
        file = request.FILES['file_input']
        print(file)
        transcription_audio(file)

    return render(request, 'linteq_app/index.html', context=context)
