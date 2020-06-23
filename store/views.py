from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from PIL import Image

from .forms import RegisterForm, LoginForm, AccountForm
from .models import UserImage

# Create your views here.
ALLOWED_SPECIAL_CHAR = ['_', '@', '$', '#']


def store(request):
    frontend = {}
    return render(request, 'store/store.html', frontend)

def cart(request):
    frontend = {}
    return render(request, 'store/cart.html', frontend)

def checkout(request):
    frontend = {}
    return render(request, 'store/checkout.html', frontend)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            check = form.cleaned_data['checkpwd']

        if User.objects.filter(email=email).first():
            form.errors['email'] = ["Email ID already registered with us."]

        elif password != check:
            form.errors['password'] = ["Passwords must match!"]

        elif len(password) < 8                                                          \
        or not any(char.isdigit() for char in password)                                 \
        or not any(char.isupper() for char in password)                                 \
        or not any(char.islower() for char in password)                                 \
        or not any(not char.isalnum() for char in password)                             \
        or not any(char in ALLOWED_SPECIAL_CHAR for char in password):
            form.errors['password'] = ["Password does not match criteria."]

        else:
            new_user = User.objects.create_user(username, email, password)
            UserImage.objects.create(user=new_user)
            return redirect('login')

    else:
        form = RegisterForm()

    frontend = {'form': form}
    return render(request, 'store/register.html', frontend)

def cust_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)

            except ObjectDoesNotExist:
                form.errors['username'] = ["Username not registered with us."]

            else:
                if not user.check_password(password):
                    form.errors['password'] = ["Incorrect password entered."]

                else:
                    login(request, user)
                    
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('store')
    
    else:
        form = LoginForm()

    frontend = {'form': form}
    return render(request, 'store/login.html', frontend)

@login_required
def myorders(request):
    frontend = {}
    return render(request, 'store/myorders.html', frontend)

@login_required
def account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            check = form.cleaned_data['checkpwd']
            pic = form.cleaned_data['profile_pic']

            if email:
                if email == user.email:
                    form.errors['email'] = ['Email ID is already this.']

                elif User.objects.filter(email=email):
                    form.errors['email'] = ["Email ID already registered with us."]

                else:
                    user.email = email
                    user.save(update_fields=['email'])
                    return redirect('account')

            if username:
                if username == user.username:
                    form.errors['username'] = ["Username is already this."]

                elif User.objects.filter(username=username):
                    form.errors['username'] = ["A user with this username already exists."]

                else:
                    user.username = username
                    user.save(update_fields=['username'])
                    return redirect('account')

            if password:
                if user.check_password(password):
                    form = AccountForm()
                    form.errors['password'] = ["New password cannot be same as current password."]

                elif not check:
                    form = AccountForm()
                    form.errors['checkpwd'] = ["Please re-enter this as well to update password."]

                elif len(password) < 8                                                          \
                or not any(char.isdigit() for char in password)                                 \
                or not any(char.isupper() for char in password)                                 \
                or not any(char.islower() for char in password)                                 \
                or not any(not char.isalnum() for char in password)                             \
                or not any(char in ALLOWED_SPECIAL_CHAR for char in password):
                    form = AccountForm()
                    form.errors['password'] = ["Password does not match criteria."]

                elif check:
                    if password != check:
                        form = AccountForm()
                        form.errors['checkpwd'] = ["Passwords must match."]

                    else:
                        user.set_password(password)
                        user.save(update_fields=['password'])
                        return redirect('login')

            if pic:
                user = UserImage.objects.get(user=request.user)
                user.profile_pic = pic
                user.save(update_fields=['profile_pic'])

                size = (200, 200)
                pic = Image.open(user.profile_pic)
                pic.thumbnail(size)
                pic.save(user.profile_pic.path)

                return redirect('account')

    else:
        form = AccountForm()

    frontend = {'form': form}
    return render(request, 'store/account.html', frontend)

@login_required
def cust_logout(request):
    logout(request)
    return redirect('store')