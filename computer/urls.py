
from os import name
import django
from django.urls import path
from django.contrib.auth.decorators import permission_required
from .views import ComputerDelView, ComputerDetail, ComputerUpdateView, ComputerView, import_cart_data, import_data

urlpatterns = [
    path('',ComputerView.as_view(), name='list'),
    path('<int:pk>', ComputerDetail.as_view(), name='computerdetail'),
    path("<int:pk>/update", ComputerUpdateView.as_view(), name='computerupdate'),
    path('<int:pk>/delete', ComputerDelView.as_view(), name='computerdeltete'),
    path('import/', import_data, name='import'),
    path('import-cart/', import_cart_data, name='importcart')
]
