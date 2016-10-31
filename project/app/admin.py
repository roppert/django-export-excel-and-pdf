from django.contrib import admin

from .models import Temperature, WeatherStation


admin.site.register(Temperature)
admin.site.register(WeatherStation)
