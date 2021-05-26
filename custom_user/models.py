from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10, null=False, validators=[RegexValidator('^[0-9\-\+]{9,15}$')])