
import os
import csv
import ast
import datetime
import json
from django.db import models

from django.db.models.fields import NullBooleanField
from django.http import response
from django.http.response import HttpResponseNotFound
from django.views.generic import ListView, DetailView, UpdateView
from django.core import serializers
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView

from .models import Computer
from sell_web import settings
from cart.models import Cart
from import_data.celery_task import add_cart, csv2dic, csv2model, add_list_cart, set_all_to_DO

class ComputerView(ListView):
    """
        View chinh cua web
    """
    model = Computer
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            ##https://docs.djangoproject.com/en/1.11/topics/db/queries/#querysets-are-lazy
            #https://stackoverflow.com/questions/45228187/possible-to-filter-the-queryset-after-querying-django
            # giai thich ly do khong co su khac biet khi truy cap database 
            computer_list = Computer.objects

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
            # JsonSerializer = serializers.get_serializer('json')
            # json_serializer = JsonSerializer()
            # json_serializer.serialize(computer_list)
            # data = json_serializer.getvalue()
            self.object_list = computer_list
            context = self.get_context_data()

            # return render(request, template_name='computer/computer_list.html', context= computer_list.values())
            return self.render_to_response(context)


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




def import_computer_data(filename):
    with open(filename,'r') as computer_file:
        data = computer_file.readlines()
        for i in range(len(data)):
            if i == 0:
                continue
            else:
                temp = csv2dic(data[0],data[i])
                
                if not csv2model.delay(temp):
                    return False
        return True

def import_data(request, *args, **kwargs):
    if request.user.is_authenticated and request.user.is_superuser:
        filename = ast.literal_eval(request.body.decode('UTF-8'))['filename']
        if import_computer_data(filename):
            response = HttpResponse({'Done'})
        else:
            response = HttpResponse({'Failed'})

    return response


def import_cart_data(request, *args, **kwargs):
    count = 0
    for i in range(8,1003):
        set_all_to_DO.delay(i)
        count+=1
    return HttpResponse({f'Success add {count} cart'})



class ComputerDetail(DetailView):
    model = Computer
    def get_queryset(self) -> models.query.QuerySet:
        return Computer.objects.filter()
    

class ComputerUpdateView(UpdateView):
    model = Computer
    fields = ['name', 'brand', 'core', 'ram', 'hardware', 'price', 'amount']
    template_name_suffix = '_update_form'
    
    def post(self, request, *args: str, **kwargs) -> HttpResponse:
        if request.user.is_superuser:
            self.success_url = f'/computer/{kwargs.get("pk")}'
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponse({'Nope, You can not do that'})

class ComputerDelView(DeleteView):
    model = Computer
    template_name_suffix = '_confirm_delete'


    def delete(self, request, *args: str, **kwargs) -> HttpResponse:
        if request.user.is_superuser:
            self.success_url = f'/computer'
            return super().delete(request, *args, **kwargs)
        else:
            return HttpResponse({'Nope, You can not do that'})

