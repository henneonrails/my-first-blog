from django import forms
from datetime import date
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

from .models import Schichtplan
# from django.conf import settings

# User = settings.AUTH_USER_MODEL


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name 

class SchichtplanForm(forms.ModelForm):
    datum = forms.DateField(widget=forms.SelectDateWidget(),initial = date.today())
    schichtmeister = MyModelChoiceField(queryset=User.objects.all())
    
    class Meta:
        model = Schichtplan
        fields = ['datum', 'schichtmeister']

