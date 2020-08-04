from django.urls import path
from .views import IndexView, RegistrationView, LoginView, Logout, DrinkView


urlpatterns = [
    path('', IndexView.as_view(), name=''),
    path('index/', IndexView.as_view(), name='index'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('drink/', DrinkView.as_view(), name='drink')
]