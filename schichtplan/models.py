from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Schichtplan(models.Model):
    datum = models.DateField()
    schicht = models.ForeignKey('Schichten',
                                null=True,
                                on_delete=models.SET_NULL)
    schichtmeister = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.datum)


class Schichten(models.Model):
    schicht = models.CharField(max_length=15)

    def __str__(self):
        return self.schicht


'''
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
      '''
