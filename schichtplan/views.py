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
    dateSet = calculateShiftForDate(today)
    context = {'dateSet': dateSet}
    print(context)
    template = 'schichtplan/today.html'
    return render(request, template, context)


def schichtplan_detail(request):
    return 0


def calculateShiftForDate(date):
    shiftValue = searchShiftForDate(date)
    # erzeuge einen neuen Schichtplan Eintrag mit dem Ergebenis
    # der Schichten Suche
    newShift = Schichtplan(datum=date, schicht=shiftValue)
    ## erzeuge ein Array mit zwei Tagen davor und zwei Tagen dahinter
    arrayShift = [newShift]
    newDate = date + timedelta(days=1)
    arrayShift.append(Schichtplan(
        datum=newDate,
        schicht=searchShiftForDate(newDate))
                                )
    return arrayShift


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
        print('return value')
        print(schichtplan.first().schicht)
        return schichtplan.first().schicht

    # Überprüfe ob übergebenes Datum ist kleiner als das Datum
    # des ersten Schichtplandatums
    myquery = Schichtplan.objects.order_by('datum')[0]
    if date < myquery.datum:
        return searchShiftForDate(date + interval)
    else:
        return searchShiftForDate(date - interval)
