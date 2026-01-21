from django import forms
from .models import Remedy

class RemedyForm(forms.ModelForm):
    class Meta:
        model = Remedy
        fields = ["notes", "prescription_file"]
