from django import forms


class FilePostForm(forms.Form):
    file = forms.FileField()
    # #model_type = forms.CharField()
    # #max_line_width = forms.IntegerField()
    # max_line_count = forms.IntegerField()
    # language = forms.CharField()
    file_name = forms.CharField()