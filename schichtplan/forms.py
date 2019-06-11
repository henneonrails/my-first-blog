from django import forms
from django.forms import ModelForm

from .models import Schichtplan


class SchichtplanForm(forms.Form):
    datum = forms.DateField(widget=forms.widgets.DateInput(attrs={'id': 'datepicker'}))
    
