from django.db import models



# class Core(models.Model):
#     _brand_type = [
#         ('IN', 'Intel'),
#         ('AM', 'AMD')
#     ]
#     # _intel_ver = [
#     #     ('I9', 'Intel Core I9'),
#     #     ('I7', 'Intel Core I7'),
#     #     ('I5', 'Intel Core I5'),
#     #     ('I3', 'Intel Core I3')
#     # ]
#     # _amd_ver = [
#     #     ('R9', 'AMD Ryzen 9'),
#     #     ('R7', 'AMD Ryzen 7'),
#     #     ('R5', 'AMD Ryzen 5'),
#     #     ('R3', 'AMD Ryzen 3')
#     # ]

#     brand = models.CharField(max_length=2, choices=_brand_type, null= False)
#     if brand == 'IN':
#         ver = models.CharField(max_length=2, choices=_intel_ver, null= True)
#     elif brand == 'AM':
#         ver = models.CharField(max_length=2, choices=_amd_ver, null=True)
#     def __init__(self, data, *args, **kwargs) -> None:
        

class Computer(models.Model):
    _brand_choices = [
            ('DE', 'Dell'),
            ('AS', 'Asus'),
            ('MA', 'Mac'),
            ('AC', 'Acer')
        ]

    _core_choices =[
        ('Intel', (
                    ('I9', 'Intel Core I9'),
                    ('I7', 'Intel Core I7'),
                    ('I5', 'Intel Core I5'),
                    ('I3', 'Intel Core I3') 
                )
            ),
        ('Amd', (
                    ('R9', 'AMD Ryzen 9'),
                    ('R7', 'AMD Ryzen 7'),
                    ('R5', 'AMD Ryzen 5'),
                    ('R3', 'AMD Ryzen 3')
                )
            )
    ]

    _ram_choices = [
            ('04', '4gb'),
            ('08', '8gb'),
            ('16', '16gb'),
            ('32', '32gb')
        ]
    

    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=2, choices=_brand_choices, null=False)
    core = models.CharField(max_length=2, choices=_core_choices, null=False)
    ram = models.CharField(max_length=2, choices=_ram_choices, null= False)
    hardware = models.CharField(max_length=2,
                                choices=[('05','500gb'),('10','1T')],
                                 null=False)
    price = models.DecimalField(max_digits=99, decimal_places=2)
    amount = models.PositiveIntegerField(default=0)
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return "/computer/%i" %self.id