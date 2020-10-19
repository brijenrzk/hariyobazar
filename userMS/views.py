from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Customer
# Create your views here.


def login(request):
    if request.method == 'POST':
        usernam = request.POST['username']
        passwor = request.POST['password']
        user = authenticate(request, username=usernam, password=passwor)
        print(user)
        if user is not None:
            auth.login(request, user)
            print("logged in")
            return render(request, "userMS/dashboard.html", {"usr": User.objects.get(pk=request.user.id)})

        else:
            print("error")
            return render(request, "userMS/login.html", {'error': "Worng Username and Password"})

    else:
        return render(request=request, template_name="userMS/login.html", context={})


def register(request):
    if(request.method == "POST"):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = make_password(request.POST['password'])
        username = request.POST['username']
        contact_number = request.POST['contact_number']
        dob = request.POST['dob']
        gender = request.POST['gender']

        usr = User(first_name=first_name, last_name=last_name,
                   email=email, username=username, password=password)
        usr.save()
        c = Customer(user_id=usr.id, contact=contact_number,
                     dob=dob, gender=gender)
        c.save()
        return render(request, "userMS/register.html", context={})

    else:
        return render(request, "userMS/register.html", context={})


def signout(request):
    logout(request)
    return redirect('userMS:login')


def dashboard(request):
    return render(request, "userMS/dashboard.html", {})
