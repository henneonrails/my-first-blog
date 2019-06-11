from django.shortcuts import render
import datetime
from datetime import timedelta, date
import calendar


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
    newContext = html_forSchichtplan(dateSet)
    # print(newContext)
    context = {
                'dateSet': dateSet,
                'newDateSet': newContext[0],
                'newSchichtSet': newContext[1]
                }
    template = 'schichtplan/today.html'
    return render(request, template, context)


def html_forSchichtplan(dataSet):
    newDataSetForDates = []
    newDataSetForSchicht = []
    for data in dataSet:
        datum = data.datum
        formatedDate = datum.strftime("%d.%m.%Y")
        schicht = data.schicht
        if datum == date.today():
            dateString = f"<td class=\"text-success\"> {formatedDate} </td>"
        else:
            dateString = f"<td> {formatedDate} </td>"
        schicht = f"<td> {schicht} </td>"
        newDataSetForDates.append(dateString)
        newDataSetForSchicht.append(schicht)
    return [newDataSetForDates, newDataSetForSchicht]


def schichtplan_detail(request):
    return 0


def calculateShiftForDate(datum):
    # shiftValue = searchShiftForDate(datum)
    # erzeuge einen neuen Schichtplan Eintrag mit dem Ergebenis
    # der Schichten Suche
    # newShift = Schichtplan(datum=datum, schicht=shiftValue)
    # erzeuge ein Array mit zwei Tagen davor und zwei Tagen dahinter
    arrayShift = []
    daysInMonth = calendar.monthrange(datum.year, datum.month)[1]
    for day in range(1, daysInMonth):
        newDate = date(datum.year, datum.month, day)
        arrayShift.append(Schichtplan(
                datum=newDate,
                schicht=searchShiftForDate(newDate)))
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
