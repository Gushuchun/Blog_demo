import string
import random
from django.shortcuts import render
from django.http.response import JsonResponse
from pyexpat.errors import messages
from django.core.mail import send_mail
from .models import CaptchaModel

# Create your views here.
def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def index(request):
    return render(request, 'index.html')

def send_email(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code":400, "messages":'Must be Email!'})

    captcha = "".join(random.sample(string.digits,6))
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha':captcha})
    send_mail("AOA Blog Registration Verification", message=f"Your Verification Code is: {captcha}", from_email=None, recipient_list=[email])
    return JsonResponse({"code":200, "messages":"Verification Code Sent Successfully"})
