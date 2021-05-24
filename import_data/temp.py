# import random
# from cart.models import Cart
# from custom_user.models import CustomUser
# from django.core.exceptions import ValidationError

# def add_list_cart():
#     dic = {}
#     dic['count'] = random.randint(1,7)
#     # dic['user_create'] = CustomUser.objects.get(id = '1')
#     for i in range(dic['count']):
#         dic[f'computer_{i}'] = {
#             'computer_id': str(random.randint(1,83)),
#             'number': str(random.randint(1,20))
#         }
#     cart = Cart()
#     cart.user_create = CustomUser.objects.get(id = str(random.randint(1,3)))
#     cart.list_computer = dic
#     cart.update_total_amount()
#     try:
        
#         cart.full_clean()
#     except ValidationError as e:
#         print('error in Validation model', e)
#         return False
#     else:
#         cart.save()
#         return True
