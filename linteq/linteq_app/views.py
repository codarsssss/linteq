from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        'title': 'Linteq'
    }
    return render(request, 'linteq_app/index.html', context=context)
