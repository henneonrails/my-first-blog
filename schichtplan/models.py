from django.db import models


class Schichtplan(models.Model):
  datum = models.DateField()
  schicht = models.CharField(max_length=20)


class Schichten(models.Model):
  schicht = [
    'Früh',
    'Spät',
    'Nacht',
    'Frei',
    'Vario',
    'Früh12',
    'Nacht12',
    'VarioFrüh',
    'VarioSpät',
    'VarioNacht',
    'VarioFrüh12',
    'VarioNacht12',
    ]
  # Früh, Spät, Nacht, Früh12, Nacht12, Frei, Vario,
