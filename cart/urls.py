from django.urls import path

from .views import CartDetailView, CartListView, CartUpdateView, get_report
from computer.views import ReportDetail


urlpatterns =[
    path('', CartListView.as_view(), name='cartlist'),
    path('<int:pk>', CartDetailView.as_view(), name='cartdetail'),
    path('<int:pk>/update', CartUpdateView.as_view(), name='cartupdate'),
    path('report', get_report, name='report'),
    path('report/<str:filename>', ReportDetail.as_view())
]
