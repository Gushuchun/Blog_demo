from django.urls import path
from . import  views

app_name = 'author'

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('index', views.index, name='index'),
    path('captcha', views.send_email, name='email_captcha'),
]