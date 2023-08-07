from django import forms

from .models import Consultation


class ConsultationForm(forms.ModelForm):

    class Meta:
        model = Consultation
        fields = ['name', 'email', 'subject', 'message']


class FilePostForm(forms.Form):
    file = forms.FileField()
    translate_checkBox = forms.CharField(required=False)
    translate_language = forms.CharField(required=False)
    file_name = forms.CharField(required=False)
