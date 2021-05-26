import os
import csv
import datetime

from sell_web import settings
from django.views.generic import DetailView
from django.shortcuts import HttpResponse, redirect
from django.http.response import HttpResponseNotFound

from .generate_report import Report


class ReportDetail(DetailView):
    
    def get(self, request, *args, **kwargs):
        file_name = kwargs.get('filename', None)
        if request.user.is_superuser:
            if file_name is not None:
                try:
                    data = {}
                    with open(os.path.join(settings.BASE_DIR, 'report_file',file_name), 'r') as file:
                        file_data = csv.DictReader(file)
                        for rows in file_data:
                            key = rows['No']
                            data[key] = rows
                        print(data)
                    response = HttpResponse(str(data), content_type = 'application/vnd.ms-excel')
                    response['Content-Disposition'] = f'attachment; filename = {file_name}'
                except IOError:
                    response = HttpResponseNotFound('<h1>File not exist</h1>')
            return response
        else:
            return HttpResponse({'Nope, You can not do that'})

def get_report(request, *args, **kwargs):
    if request.user.is_staff:
        begin = request.GET.get('begin', None)
        end = request.GET.get('end', None)
        path_out = request.GET.get('path_out', None)
        if begin is not None and end is not None:
            if datetime.datetime.strptime(end, "%Y-%m-%d").date() <= datetime.date.today():
                report = Report(begin, end, path_out=path_out)
                reportname = report.get_query(request)
                return redirect(f'/report/{reportname}')
            else:
                return HttpResponse({'end date hasn\'t pass yet'})
        else:
            return HttpResponse({'begin and end is none'})
    else:
        return HttpResponse({'Nope, You can not do that'})