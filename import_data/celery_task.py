from order.models import Order
from computer.models import Computer
from .import_data import app
from django.core.exceptions import ValidationError
import re
import random
from custom_user.models import CustomUser

@app.task()
def csv2model(csv_line):
    computer = Computer(
        name = csv_line['name'],
        brand = csv_line['brand'],
        core = csv_line['core'],
        ram = csv_line['ram'],
        hardware = csv_line['hardware'],
        price = int(csv_line['price']),
        amount = int(csv_line['amount'])
    )
    try:
        
        computer.full_clean()
    except ValidationError as e:
        print('error in Validation model', e)
        return False
    else:
        computer.save()
        return True

def csv2dic(head, text):
    head=head.replace('\n','')
    text=text.replace('\n','')
    head = re.split(',', head)
    text = re.split(',', text)
    dic = {}
    for i in range(len(head)):
        dic[head[i]] = text[i]
    return dic


@app.task()
def add_order(csv_line):
    order = Order(
        user_create = csv_line['id_user'],
        date_create = csv_line['date_create'],
        list_computer = csv_line['list_computer'],
        status = csv_line['status']
    )
    try:
        
        order.full_clean()
    except ValidationError as e:
        print('error in Validation model', e)
        return False
    else:
        order.save()
        return True
@app.task()
def add_list_order():
    dic = {}
    dic['count'] = random.randint(1,7)
    # dic['user_create'] = CustomUser.objects.get(id = '1')
    for i in range(dic['count']):
        dic[f'computer_{i}'] = {
            'computer_id': str(random.randint(1,76)),
            'number': str(random.randint(1,20))
        }
    order = Order()
    order.user_create = CustomUser.objects.get(id = str(random.randint(1,3)))
    order.list_computer = dic
    order.update_total_amount()
    try:
        
        order.full_clean()
    except ValidationError as e:
        print('error in Validation model', e)
        return False
    else:
        order.save()
        return True
@app.task
def set_all_to_DO(orderid):
    order = Order.objects.get(id = str(orderid))
    order.status = 'DO'
    try:
        order.full_clean()
    except ValidationError as e:
        print('error in Validation model', e)
        return False
    else:
        order.save()
        return True