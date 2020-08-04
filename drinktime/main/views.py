from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import RegistrationForm, LoginForm, DrinkForm
from django import forms
from main.models import Drink


class IndexView(LoginRequiredMixin, View):
    """ Логика главной страницы """

    def get(self, request):
        user = request.user
        username = user.username
        drinks = Drink.objects.filter(user=user)

        return render(request, 'main/index.html', context={
                                                'user': username,
                                                'drinks': drinks,
                                                    })

class LoginView(View):
    """ Логика пользовательских логинов """

    def get(self, request):
        form = LoginForm()
        return render(request, 'main/login.html', context={'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            form = LoginForm(request.POST)

            if form.is_valid():
                user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
                if not user:
                    return redirect(reverse_lazy('login'))
                login(request, user)
                return redirect(reverse_lazy('index'))
        else:
            redirect(reverse_lazy('index'))


class Logout(LogoutView):
    """ Логика пользовательского логаута """

    next_page = 'login'


class RegistrationView(FormView):
    """ Логика страницы регистрации пользователей """
    
    template_name = 'main/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        User.objects.create_user(
                                username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'],
                                email=form.cleaned_data['email'])
        return super().form_valid(form)

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'main/registration.html', {'form':RegistrationForm()})
        else:
            return redirect(reverse_lazy('index'))

class DrinkView(LoginRequiredMixin, FormView):
    """ Логика страницы с напитками """
    
    template_name = 'main/drink.html'
    form_class = DrinkForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        Drink.objects.create(
                            drink_name=form.cleaned_data['drink_name'],
                            drink_time=form.cleaned_data['drink_time'],
                            volume=form.cleaned_data['volume'],
                            user=self.request.user)
        return super().form_valid(form)

    def get(self, request):
        return render(request, 'main/drink.html', context={'form':DrinkForm()})



    

