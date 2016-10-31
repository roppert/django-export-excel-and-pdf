from django.db import models


class WeatherStation(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Temperature(models.Model):
    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE)
    date = models.DateField()
    max = models.DecimalField(max_digits=4, decimal_places=1)
    mean = models.DecimalField(max_digits=4, decimal_places=1)
    min = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return str(self.date)
