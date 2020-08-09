from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import RegistrationForm, LoginForm, DrinkForm
from django import forms
from main.models import Drink, User, Follows


class IndexView(LoginRequiredMixin, View):
    """ Логика главной страницы """

    def get(self, request):
        user = request.user
        my_drinks = Drink.objects.filter(user=user)  # получение своей информации
        followed_drinks = Drink.objects.filter(user__followers__follower__pk=user.pk)  # получение информации из подписок
        drinks = my_drinks.union(followed_drinks).order_by('-drink_time')
        return render(request, 'main/index.html', context={
                                                'user': user,
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


class ProfileView(LoginRequiredMixin, View):
    """ Логика страницы пользователя """

    def get(self, request, id):

        try:
            user = User.objects.get(pk=id)
            followers = [f.follower for f in user.followers.all()]
            drinks = Drink.objects.filter(user=user)
        
        except User.DoesNotExist:
            return HttpResponse(content='User not found', status=404)

        return render(request, 'main/user.html', context={
                                                        'user': user,
                                                        'followers': followers,
                                                        'drinks': drinks
                                                        })


class FollowView(LoginRequiredMixin, View):
    """ Логика подписки на пользователя """

    def get(self, request, id):

        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return HttpResponse(content='User not found', status=404)

        if request.user != user:
            request.user.follow(user)
        else:
            return HttpResponse(content='You cant follow yourself', status=400)

        return redirect(f'/user/{id}/')


class UnfollowView(LoginRequiredMixin, View):
    """ Логика подписки на пользователя """

    def get(self, request, id):

        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return HttpResponse(content='User not found', status=404)
        
        if request.user != user:
            request.user.unfollow(user)
        else:
            return HttpResponse(content='You cant unfollow yourself', status=400)

        return redirect(f'/user/{id}/')



    

