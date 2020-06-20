from django.shortcuts import render

# Create your views here.
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
    frontend = {}
    return render(request, 'store/register.html', frontend)

def cust_login(request):
    frontend = {}
    return render(request, 'store/login.html', frontend)

def myorders(request):
    frontend = {}
    return render(request, 'store/myorders.html', frontend)

def account(request):
    frontend = {}
    return render(request, 'store/account.html', frontend)

def cust_logout(request):
    frontend = {}
    return render(request, 'store/store.html', frontend)