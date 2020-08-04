from django import forms
from main.models import Drink
from django.utils import timezone


class RegistrationForm(forms.Form):
	""" Форма регистрации новых пользователей """

	username = forms.CharField(max_length=16, min_length=6)
	password = forms.CharField(max_length=32, min_length=4, widget=forms.PasswordInput)
	password2 = forms.CharField(max_length=32, min_length=4, widget=forms.PasswordInput)
	email = forms.EmailField(max_length=32, min_length=6)

	def clean(self):
		""" Переопределение метода валидации - для поля подтверждения пароля """
		
		cleaned_data = super(RegistrationForm, self).clean()
		password = cleaned_data['password']
		password2 = cleaned_data['password2']
		if password != password2:
			raise forms.ValidationError("Password and confirm password does not match !")


class LoginForm(forms.Form):
	""" Форма для логина пользователей """

	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


class DrinkForm(forms.ModelForm):
	""" Форма для указания какой напиток выпил """

	class Meta:
		model = Drink
		fields = ['drink_name', 'drink_time', 'volume']

	def clean(self):
		""" Переопределение метода валидации, чтобы нельзя было указать будущее время """

		cleaned_data = super(DrinkForm, self).clean()
		if cleaned_data['drink_time'] > timezone.now():
			raise forms.ValidationError('Please enter present or past tense in drink time')
