from django.shortcuts import render
import datetime
from datetime import timedelta


from .models import Schichtplan, Schichten


def schichtplan_list(request):
    # dateSet = buildDateArray(today)
    dateSet = Schichtplan.objects.all()
    context = {'dateSet': dateSet}
    template = 'schichtplan/list.html'
    return render(request, template, context)


def schichtplan_today(request):
    today = datetime.date.today()
    dateSet = searchShiftForDate(today)
    context = {'dateSet': dateSet}
    template = 'schichtplan/today.html'
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


def searchShiftForDate(date):
    numberOfSchiftdays = len(Schichtplan.objects.all())
    interval = timedelta(days=numberOfSchiftdays)
    schichtplan = Schichtplan.objects.filter(datum=date)
    print(date)
    if schichtplan:
        print(schichtplan)
        return schichtplan

    # Überprüfe ob übergebenes Datum ist kleiner als das Datum
    # des ersten Schichtplandatums
    myquery = Schichtplan.objects.order_by('datum')[0]
    if date < myquery.datum:
        searchShiftForDate(date + interval)
    else:
        searchShiftForDate(date - interval)
