from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.http import HttpResponse



class User(AbstractUser):
	""" Расширение стандартной модели пользователя """

	def follow(self, user):
		""" Логика подписки на пользователя """
		f = Follows.objects.create(follower=self, followed=user)
		f.save()

	def unfollow(self, user):
		f = Follows.objects.get(follower=self, followed=user)
		f.delete()

	def det_row(self):
		""" Функция для определения дней подряд """
		pass

class Drink(models.Model):
    """ Класс напитков пользователя """
    
    drink_name = models.CharField(max_length=16, blank=True)
    drink_time = models.DateTimeField(default=timezone.now())
    volume = models.DecimalField(max_digits=3, decimal_places=1, blank=True, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drinks')


class Follows(models.Model):
	""" Таблица ассоциаций подписчик - подписант """

	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followeds')
	""" Тот кто подписывается """

	followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
	""" Тот на кого подписываются """

	""" Followers.objects.create(follower=u1, followed = u2) - ситуация когда u1 подписывается на u2 """

	""" Для доступа к подписчикам ---> u2.followers.all() """

	""" Для доступа к тем на кого подписан ---> u2.followeds.all() """