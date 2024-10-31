import string
import random
import re

from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm,LoginForm
from django.contrib.auth import get_user_model,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

User = get_user_model()


# Create your views here.
@require_http_methods(['GET', 'POST'])
def a_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # login
                login(request, user)
                # judge if the user needs to remember me
                if not remember:
                    # If not click, then need to log in again when the browser closes
                    request.session.set_expiry(0)
                # If clicked, nothing is done, using the default two-week expiration time
                return redirect('/')
            else:
                print("Email or password error")
                form.add_error('email', 'Email or password error')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            User.objects.create_user(username=username, email=email, password=password)
            return render(request, 'login.html', {'form': form})
        else:
            print(form.errors)
            return render(request, 'register.html', {'form': form})


def index(request):
    return render(request, 'index.html')


def send_email(request):
    email = request.GET.get('email')

    # A regular expression used to validate the mailbox
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Check if the mailbox is empty or formatted incorrectly
    if not email or not re.match(email_regex, email):
        return JsonResponse({"code": 400, "message": 'Please enter a valid email address.'})

    # Generate a 6-digit verification code
    captcha = "".join(random.sample(string.digits, 6))

    # Save the verification code to the database
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})

    # Send an email with a verification code
    send_mail(
        "AOA Blog Registration Verification",
        message=f"Your verification code is: {captcha}",
        from_email=None,
        recipient_list=[email]
    )

    return JsonResponse({"code": 200, "message": "Verification Code Sent Successfully"})

def a_logout(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)  # 保存文件
        # 在这里可以添加更新用户头像的逻辑
        return JsonResponse({'message': 'Image uploaded successfully!', 'filename': filename})
    return JsonResponse({'error': 'Invalid request'}, status=400)