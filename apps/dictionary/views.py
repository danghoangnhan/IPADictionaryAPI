from django.http import HttpResponse
from django.shortcuts import render
from tablib import Dataset

from apps.dictionary.models import Dictionary
from apps.dictionary.resources import DictionaryResource


def home_view(request):
    return render(request, 'base.html')


def export_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = DictionaryResource()
        dataset = employee_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response

    return render(request, 'export.html')


def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = DictionaryResource()
        dataset = Dataset()
        new_employees = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(new_employees.read().decode('utf-8'), format='csv')
            result = employee_resource.import_data(dataset, dry_run=True)
        elif file_format == 'JSON':
            imported_data = dataset.load(new_employees.read().decode('utf-8'), format='json')
            result = employee_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            employee_resource.import_data(dataset, dry_run=False)

    return render(request, 'import.html')
