from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone


class Drink(models.Model):
    """ Класс напитков пользователя """
    
    drink_name = models.CharField(max_length=16, blank=True)
    drink_time = models.DateTimeField(default=timezone.now())
    volume = models.DecimalField(max_digits=3, decimal_places=1, blank=True, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, )