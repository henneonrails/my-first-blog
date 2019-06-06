from django.db import models


class Schichtplan(models.Model):
    datum = models.DateField()
    schicht = models.ForeignKey('Schichten',
                                null=True,
                                on_delete=models.SET_NULL)

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
