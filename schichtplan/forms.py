from django import forms
from django.forms import ModelForm
from datetime import date

from .models import Schichtplan


class SchichtplanForm(forms.ModelForm):
    datum = forms.DateField(initial=date.today())
    
    class Meta:
        model = Schichtplan
        fields = ['datum', 'schichtmeister']
        