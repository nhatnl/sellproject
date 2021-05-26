import os
import csv

from order.models import Order
from sell_web import settings
from django.db import models
from computer.models import Computer


def list_sort_custom(dic):
    return dic['computer_selled']


class Report:
    begin = models.DateField(default=None)
    end = models.DateField(default=None)
    path_out = os.path.join(settings.BASE_DIR, 'report_file')
    model = Order

    def __init__(self, begin, end, /, path_out=None) -> None:
        self.begin = begin
        self.end = end
        if path_out is not None:
            self.path_out = path_out

    def get_query(self, request):
        querry = self.model.objects.all().filter(status='DO').filter(
            date_create__range=(self.begin, self.end))
        report = []
        for i in querry:
            computer_list = i.list_computer
            for j in range(int(computer_list['count'])):
                index = 'computer_' + str(j)
                computer = Computer.objects.get(
                    id=computer_list[index]['computer_id'])
                if request.GET.get('brand', None) is not None:
                    if computer.brand != request.GET.get('brand'):
                        continue
                if request.GET.get('core', None) is not None:
                    if computer.core != request.GET.get('core'):
                        continue
                if request.GET.get('ram', None) is not None:
                    if computer.ram != request.GET.get('ram'):
                        continue
                if request.GET.get('hardware', None) is not None:
                    if computer.hardware != request.GET.get('hardware'):
                        continue
                key = False
                for k in range(len(report)):
                    if report[k]['name'] == computer.name:
                        report[k]['computer_selled'] += int(
                            computer_list[index]['number'])
                        report[k]['profit'] = report[k]['computer_selled'] * \
                            computer.price
                        key = True
                if key:
                    pass
                else:
                    report.append({
                        'name': computer.name,
                        'computer_selled': int(computer_list[index]['number']),
                        'profit': computer.price * int(computer_list[index]['number'])
                    })

        report.sort(key=list_sort_custom, reverse=True)
        try:
            with open(os.path.join(self.path_out,
                                   f'report_{[request.GET.get(i) for i in request.GET]}.csv'),
                                    'w') as f:
                writer = csv.DictWriter(
                    f, fieldnames=['No', 'name', 'computer_selled', 'profit'])
                writer.writeheader()
                for i, row in enumerate(report):
                    if i == 10:
                        break
                    report[i]['No'] = i + 1
                    writer.writerow(row)
                return f'report_{[request.GET.get(i) for i in request.GET]}.csv'
        except IOError:
            print('I/O Error')
        return False
