from django.shortcuts import render
from .trascription_logic import transcript_file
from .forms import FilePostForm

# Create your views here.


def index(request):

    if request.method == "POST" and request.FILES:
        form = FilePostForm(request.POST, request.FILES)
        if form.is_valid():
            form_object = form.cleaned_data
            
            return render(request, 'linteq_app/index.html', context={
                                                                'result': transcript_file(form_object['file'], 
                                                                form_object['file_name'],
                                                                str(form_object['file']).split('.')[-1])})
        else:
            form = FilePostForm()
    
    return render(request, 'linteq_app/index.html')

