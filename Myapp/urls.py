from django.urls import path, include
from .views import home
from .views import *
from django.contrib.auth import views as auth_view

urlpatterns = [
    #path('',home,name='home'),
    path('', HomePageView.as_view(), name = 'home'),
	path('mail/', send_email, name='mail'),
    path('bot_view/', bot_search, name='bot_search'),
    path('register/', register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name = 'Myapp/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name = 'Myapp/logout.html'), name='logout'),
]