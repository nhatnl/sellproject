from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.core.exceptions import FieldError, ValidationError

from .models import CustomUser
class CreateCustomUser(CreateView):
    model = CustomUser
    fields = ['username', 'password', 'phone_number']
    # template_name_suffix = '_signup_form'
    template_name = 'registration/customuser_signup_form.html'
    success_url = 'computer/'

    def post(self, request, *args: str, **kwargs ):
        if request.POST.get('username', None) is not None \
                    and request.POST.get('password', None) is not None \
                    and request.POST.get('phone_number', None):
            user = CustomUser(username = request.POST.get('username'),
                                phone_number = request.POST.get('phone_number'))
            try:
                user.set_password(request.POST.get('password'))
                user.full_clean()
            except ValidationError:
                return HttpResponse({'Validate Error'})
            user.save()
            return redirect('/')
        else:
            return HttpResponse({'Not True'})