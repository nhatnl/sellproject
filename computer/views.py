
import os
import csv

from django.db.models.fields import NullBooleanField
from django.http.response import HttpResponseNotFound
from django.views.generic import ListView, DetailView
from django.core import serializers
from django.shortcuts import HttpResponse

from .models import Computer
from sell_web import settings
from cart.models import Cart

class ComputerView(ListView):
    """
        View chinh cua web
    """
    model = Computer
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            computer_list = Computer.objects.all()
            # bat dau phan loc du lieu, cu moi thuoc tinh khac none tuc la duoc loc theo no
            # tru price, amount se duoc xem la sap xep tang dan hoac giam dan.
            if request.GET.get('brand', None) is not None:
                computer_list = computer_list.filter(
                    brand=request.GET.get('brand'))

            if request.GET.get('core', None) is not None:
                computer_list = computer_list.filter(
                    core=request.GET.get('core'))

            if request.GET.get('ram', None) is not None:
                computer_list = computer_list.filter(
                    ram=request.GET.get('ram'))

            if request.GET.get('hardware', None) is not None:
                computer_list = computer_list.filter(
                    hardware=request.GET.get('hardware'))
            # Phan order_by
            if request.GET.get('ob_price', 'ASC') == 'ASC':
                computer_list = computer_list.order_by('price', 'amount')
            else:
                computer_list = computer_list.order_by('-price', 'amount')
            # serializer data thanh dang json va response 
            JsonSerializer = serializers.get_serializer('json')
            json_serializer = JsonSerializer()
            json_serializer.serialize(computer_list)
            data = json_serializer.getvalue()
            return HttpResponse(data)


    def post(self, request, *args, **kwargs):
        """
            Input: request chua danh sach cac computer va so luong mua
            Output: id cua cart do.
        """
        if request.method == 'POST':
            if request.user.is_authenticated:
                cart = Cart()
                cart.add_to_cart(request)
                cart.full_clean()
                cart.save()
                return HttpResponse({'Done, Cart created id: %s' % cart.id})
            else:
                return HttpResponse({'Authentication not set, login first'})

class ReportDetail(DetailView):

    def get(self, request, *args, **kwargs):
        file_name = kwargs.get('filename', None)
        if file_name is not None:
            try:
                data = {}
                with open(os.path.join(settings.BASE_DIR, 'report',file_name), 'r') as file:
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
