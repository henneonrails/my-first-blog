# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta, date

import locale
import datetime
import calendar


from .models import Schichtplan, Schichten
from .forms import SchichtplanForm


def schichtplan_list(request):
    # dateSet = buildDateArray(today)
    dateSet = Schichtplan.objects.all()
    context = {'dateSet': dateSet}
    template = 'schichtplan/list.html'
    return render(request, template, context)


def schichtplan_detail(request):
    return 0