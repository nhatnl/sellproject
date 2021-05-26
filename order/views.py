
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, UpdateView
from django.db.models import QuerySet
from django.http import Http404
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView

from .models import Order



class OrderDetailView(DetailView):
    model = Order

    def get_queryset(self, request, **kwargs) -> QuerySet:
        return Order.objects.filter(user_create=request.user.id, id = kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, user_create=request.user.id, id = kwargs.get('pk') )
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class OrderListView(ListView):
    model = Order

    def get_queryset(self, request) -> QuerySet:
        return Order.objects.filter(user_create=request.user.id)

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


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['list_computer']

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_object = get_object_or_404(Order, id=kwargs.get('pk'))
            if order_object.status not in ['CR', 'PS']:
                return HttpResponse({'The Order has been confirm, \
                                        can not be update or change any more'})
            else:
                id = order_object.update_order(request)
                return HttpResponse({'Update success card id: %s' % id})
        else:
            return HttpResponse({'Login First'})

class OrderCreateView(CreateView):
    model = Order

    def post(self, request, *args: str, **kwargs) -> HttpResponse:
        """
            Input: request chua danh sach cac computer va so luong mua
            Output: id cua order do.
        """
        if request.method == 'POST':
            if request.user.is_authenticated:
                order = Order()
                order.add_to_order(request)
                order.full_clean()
                order.save()
                redirect_url = f'order/{order.id}/'
                return redirect(order)#HttpResponse({'Done, Order created id: %s' % order.id})
            else:
                return HttpResponse({'Authentication not set, login first'})
        else:
            return HttpResponse({'Method not allowed'})


