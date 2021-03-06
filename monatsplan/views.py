from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta, date

import locale
import datetime
import calendar


from schichtplan.models import Schichtplan, Schichten
from schichtplan.forms import SchichtplanForm


class MonatsplanView(View):
    template_name = "monatsplan/today.html"

    def get(self, request):
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
    locale.setlocale(locale.LC_ALL, 'de_DE')
    for data in dataSet:
        datum = data.datum
        formatedDate = datum.strftime("%d.%m.%y")
        day_of_week = calendar.day_name[datum.weekday()]
        schicht = data.schicht
        if datum == date.today():
            dateString = f"<td class=\"text-success\"> {formatedDate} <p> {day_of_week} </p> </td>"
        else:
            dateString = f"<td class'col-4'> {formatedDate} <p> {day_of_week} </p></td>"
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
    if schicht.schicht == "Früh" or schicht.schicht == "Früh12":
        schicht = f"<td bgcolor='#F9E79F'> {schicht} </td>"
    elif schicht.schicht == "Spät":
        schicht = f"<td bgcolor='#e24d7f'> {schicht} </td>"
    elif schicht.schicht == "Nacht" or schicht.schicht == "Nacht12":
        schicht = f"<td bgcolor='#4286f4'> {schicht} </td>"
    elif schicht.schicht == "Vario":
        schicht = f"<td bgcolor='#e5bcc9'> {schicht} </td>"
    else:
       schicht = f"<td> {schicht} </td>"
    return schicht





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

