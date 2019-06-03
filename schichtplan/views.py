from django.shortcuts import render
import datetime
from datetime import timedelta


from .models import Schichtplan, Schichten


def schichtplan_list(request):
    today = datetime.date.today()
    dateSet = buildDateArray(today)
    context = {'dateSet': dateSet}
    template = 'schichtplan/list.html'
    return render(request, template, context)


def schichtplan_detail(request):
    return 0


def calculate_schicht(datum_locl):
    # datum = date object
    querySchichtplan = Schichtplan.objects.filter(datum=datum_locl)
    if querySchichtplan:
        return querySchichtplan.schicht
    return "nix"


def buildDateArray(date):
    dateNew = date + timedelta(days=30)
    returnDates = []
    while date != dateNew:
        returnDates.append(date)
        date = date + timedelta(days=1)

    return returnDates
