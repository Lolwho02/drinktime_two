from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name=''),
    path('index/', IndexView.as_view(), name='index'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('drink/', DrinkView.as_view(), name='drink'),
    path('user/follow/<int:id>/', FollowView.as_view(), name='follow_function'),
    path('user/unfollow/<int:id>/', UnfollowView.as_view(), name='unfollow_function'),
    path('user/<int:id>/', ProfileView.as_view(), name='profile'),
]