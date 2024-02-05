# forms.py
from django import forms
from .models import UserFile


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UserFile
        your_file_field = forms.FileField(label="Your Label Here")
        fields = ["file"]
