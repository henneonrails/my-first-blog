from django import forms
from django.forms import ModelForm

from .models import Schichtplan


class SchichtplanForm(forms.ModelForm):
    datum = forms.DateField(widget=forms.widgets.DateInput(attrs={'class': 'datepicker'}))
    
    class Meta:
        model = Schichtplan
        fields = ['datum']
        widgets = { 'datum': forms.DateInput(attrs={'class': 'datepicker'})}