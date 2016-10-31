from django import forms

from .models import WeatherStation, Temperature


def available_stations():
    return WeatherStation.objects.values_list("id", "name")


class SearchForm(forms.Form):
    station = forms.ChoiceField(
        label="Station",
        choices=available_stations
    )
    date_from = forms.DateField(
        label="From",
        input_formats=['%Y-%m-%d',],
        widget=forms.TextInput(attrs={'size': 10}),
        required=False
    )
    date_to = forms.DateField(
        label="To",
        input_formats=['%Y-%m-%d',],
        widget=forms.TextInput(attrs={'size': 10}),
        required=False
    )

    def search(self):
        station = self.cleaned_data.get('station', None)
        date_from = self.cleaned_data.get('date_from', None)
        date_to = self.cleaned_data.get('date_to', None)

        data = Temperature.objects.filter()

        if station:
            data = data.filter(station=station)
        if date_from:
            data = data.filter(date__gte=date_from)
        if date_to:
            data = data.filter(date__lte=date_to)

        return data


