# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from datetime import timedelta, date


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


def schichtplan_today(request):
    today = datetime.date.today()
    if request.POST:
        form = SchichtplanForm(request.POST)
        if form.is_valid():
            today = form.cleaned_data['datum']
    else:
        form = SchichtplanForm()
    dateSet = calculateShiftForDate(today)
    newContext = html_forSchichtplan(dateSet)
    # print(newContext)
    # cal = calendar.LocaleHTMLCalendar(locale='de_DE')
    # html = cal.formatmonth(2019, 6)
    context = {
                'newDateSet': newContext,
                'form': form,
                }
    template = 'schichtplan/today.html'
    return render(request, template, context)


def html_forSchichtplan(dataSet):
    newDataSetForDates = []
    newDataSetForSchicht = []
    completeDataSet = []
    for data in dataSet:
        datum = data.datum
        formatedDate = datum.strftime("%d.%m.%y")
        schicht = data.schicht
        if datum == date.today():
            dateString = f"<td class=\"text-success\"> {formatedDate} </td>"
        else:
            dateString = f"<td> {formatedDate} </td>"
        schicht = setColor(schicht)
        # schicht = f"<td> {schicht} </td>"
        if datum.weekday() == 6:
            dateString = dateString + "</tr><tr>"
            schicht = schicht + "</tr><tr>"
            newDataSetForDates.append(dateString)
            newDataSetForSchicht.append(schicht)
            completeDataSet.append(''.join(newDataSetForDates))
            completeDataSet.append(''.join(newDataSetForSchicht))
            newDataSetForDates.clear()
            newDataSetForSchicht.clear()
        else:
            newDataSetForDates.append(dateString)
            newDataSetForSchicht.append(schicht)
    
    dateString = dateString + "</tr><tr>"
    schicht = schicht + "</tr><tr>"
    newDataSetForDates.append(dateString)
    newDataSetForSchicht.append(schicht)
    completeDataSet.append(''.join(newDataSetForDates))
    completeDataSet.append(''.join(newDataSetForSchicht))
    return completeDataSet


def setColor(schicht):
    if schicht.schicht == "Früh":
        schicht = f"<td bgcolor='#F9E79F'> {schicht} </td>"
    else:
       schicht = f"<td> {schicht} </td>"
    return schicht


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
    # print(date)
    if schichtplan:
        # print('return value')
        # print(schichtplan.first().schicht)
        return schichtplan.first().schicht

    # Überprüfe ob übergebenes Datum ist kleiner als das Datum
    # des ersten Schichtplandatums
    myquery = Schichtplan.objects.order_by('datum')[0]
    if date < myquery.datum:
        return searchShiftForDate(date + interval)
    else:
        return searchShiftForDate(date - interval)
