from django.test import TestCase
from datetime import date

from schichtplan.models import Schichtplan, Schichten

class SchichtplanTestCase(TestCase):

    def setUp(self):
        Schichten.objects.create(schicht = 'Früh')
        Schichtplan.objects.create(datum = date.today(), schicht = Schichten.objects.get(pk=1))

    def test_get_Schichtplan(self):
        obj = Schichtplan.objects.first()
        self.assertTrue(obj.schicht)
    
    def test_get_schichtplan_date(self):
        obj = Schichtplan.objects.filter(datum__gte=date.today())
        self.assertEqual(obj.count(), 1)
