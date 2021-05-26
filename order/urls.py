from django.urls import path

from .views import OrderCreateView, OrderDetailView, OrderListView, OrderUpdateView



urlpatterns =[
    path('', OrderListView.as_view(), name='orderlist'),
    path('new/', OrderCreateView.as_view(), name='ordercreate'),
    path('<int:pk>', OrderDetailView.as_view(), name='orderdetail'),
    path('<int:pk>/update', OrderUpdateView.as_view(), name='orderupdate'),
]
