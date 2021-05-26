from django.urls import path
from .views import ReportDetail, get_report

urlpatterns =[
    path('', get_report, name='report'),
    path('<str:filename>', ReportDetail.as_view())
]