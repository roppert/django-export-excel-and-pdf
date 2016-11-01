from django.shortcuts import render
from django.http import HttpResponse

from .forms import SearchForm
from .models import WeatherStation, Temperature
from .export.excel import WriteToExcel
from .export.pdf import WriteToPdf


def index(request):
    data = Temperature.objects.filter(station=WeatherStation.objects.first())
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.search()
    else:
        form = SearchForm()
    if 'excel' in request.POST:
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
        xlsx_data = WriteToExcel(data)
        response.write(xlsx_data)
        return response
    if 'pdf' in request.POST:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachement; filename=Report.pdf'
        pdf_data = WriteToPdf(data)
        response.write(pdf_data)
        return response
    context = {"form": form, "data": data}
    return render(request, 'app/index.html', context)
