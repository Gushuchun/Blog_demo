from django.urls import path
from . import  views

app_name = 'author'

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.a_login, name='login'),
    path('register/', views.register, name='register'),
    path('captcha', views.send_email, name='email_captcha'),
    path('logout', views.a_logout, name='logout'),
    path('upload_image/', views.upload_image, name='upload_image'),
]