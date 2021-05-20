import datetime

from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, UpdateView
from django.db import models
from django.db.models import QuerySet
from django.http import Http404
from django.utils.translation import gettext as _

from .models import Cart
from .generate_report import Report


class CartDetailView(DetailView):
    model = Cart

    def get_queryset(self) -> models.query.QuerySet:
        return Cart.objects.all()


class CartListView(ListView):
    model = Cart

    def get_queryset(self, request) -> QuerySet:
        return Cart.objects.filter(user_create=request.user.id)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset(request)
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None \
                    and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)


class CartUpdateView(UpdateView):
    model = Cart
    fields = ['list_computer']

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart_object = get_object_or_404(Cart, id=kwargs.get('pk'))
            if cart_object.status not in ['CR', 'PS']:
                return HttpResponse({'The Cart has been confirm, \
                                        can not be update or change any more'})
            else:
                id = cart_object.update_cart(request)
                return HttpResponse({'Update success card id: %s' % id})


def get_report(request, *args, **kwargs):
    begin = request.GET.get('begin', None)
    end = request.GET.get('end', None)
    path_out = request.GET.get('path_out', None)
    if begin is not None and end is not None:
        if datetime.datetime.strptime(end, "%Y-%m-%d").date() < datetime.date.today():
            report = Report(begin, end, path_out=path_out)
            reportname = report.get_query(request)
            return redirect(f'/cart/report/{reportname}')
        else:
            return HttpResponse({'end date hasn\'t pass yet'})
    else:
        return HttpResponse({'begin and end is none'})
