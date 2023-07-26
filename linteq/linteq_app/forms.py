from django import forms

from .models import Consultation


class ConsultationForm(forms.ModelForm):

    class Meta:
        model = Consultation
        fields = ['name', 'email', 'subject', 'message']


class FilePostForm(forms.Form):
    file = forms.FileField()
    model_type = forms.CharField()
    # #max_line_width = forms.IntegerField()
    # max_line_count = forms.IntegerField()
    # language = forms.CharField()
    file_name = forms.CharField(required=False)
