# import random
# from order.models import Order
# from custom_user.models import CustomUser
# from django.core.exceptions import ValidationError

# def add_list_order():
#     dic = {}
#     dic['count'] = random.randint(1,7)
#     # dic['user_create'] = CustomUser.objects.get(id = '1')
#     for i in range(dic['count']):
#         dic[f'computer_{i}'] = {
#             'computer_id': str(random.randint(1,83)),
#             'number': str(random.randint(1,20))
#         }
#     order = Order()
#     order.user_create = CustomUser.objects.get(id = str(random.randint(1,3)))
#     order.list_computer = dic
#     order.update_total_amount()
#     try:
        
#         order.full_clean()
#     except ValidationError as e:
#         print('error in Validation model', e)
#         return False
#     else:
#         order.save()
#         return True
