import ast

from django.db import models

from custom_user.models import CustomUser
from computer.models import Computer


class Cart(models.Model):
    _status_choices = [
        ('CR', 'Create'),
        ('CF', 'Confirm'),
        ('PA', 'Packing'),
        ('SH', 'Shipping'),
        ('PS', 'Pause'),
        ('DO', 'Done')
    ]

    user_create = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now=True)
    total_amount = models.DecimalField(max_digits=255, decimal_places=2)
    status = models.CharField(
        max_length=2, choices=_status_choices, default='CR')
    list_computer = models.JSONField()

    def add_to_cart(self, request, *args, **kwargs):
        """
            ham gan gia tri cho cart.
        """
        data = request.body
        data = ast.literal_eval(data.decode('UTF-8'))
        self.user_create = CustomUser.objects.get(id=request.user.id)
        self.list_computer = data['list']
        self.update_total_amount()
        return True

    def update_total_amount(self):
        """
            ham update lai gia tri total_amount theo danh sach list_computer
        """
        if self.list_computer:
            total_amount = 0
            for i in range(int(self.list_computer['count'])):
                index = 'computer_' + str(i)
                amount = Computer.objects.get(id=self.list_computer[index]['computer_id']).price \
                    * int(self.list_computer[index]['number'])
                total_amount += amount
            self.total_amount = total_amount
        return self.total_amount

    def update_status(self, status):
        """
            ham update status goc, khong kiem tra bat ky dieu kien gi
        """
        if status in self._status_choices:
            self.status = status
            return True
        else:
            return False
    
    def update_cart(self, request):
        """
            update card moi chi giu lai moi id cua card
        """
        self.update_status('CR')
        self.add_to_cart(request)
        self.full_clean()
        self.save()
        return self.id

    def confirm_card(self):
        """
            Kiem tra xem trong kho con du so luong may hay khong
            roi update lai so luong trong kho cuoi cung moi update
            status thanh CF(confirm)
        """
        for i in range(int(self.list_computer['count'])):
            index = 'computer_' + str(i)
            computer = Computer.objects.get(
                id=self.list_computer[index]['computer_id'])
            if computer is not None:
                if computer.amount - int(self.list_computer[index]['number']) < 0:
                    return False
            else:
                print('computer not found')
                raise IndexError

        for i in range(int(self.list_computer['count'])):
            index = 'computer_' + str(i)
            computer = Computer.objects.get(
                id=self.list_computer[index]['computer_id'])
            computer.amount -= int(self.list_computer[index]['number'])

        self.update_status('CF')
        return True
