from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Customer
from .forms import CreateUserForm, CreateUserForm2, UpdateUserForm, UpdateUserForm2
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.


def signIn(request):
    if request.user.is_authenticated:
        return redirect('userMS:dashboard')
    else:
        if request.method == 'POST':
            usernam = request.POST['username']
            passwor = request.POST['password']
            user = authenticate(request, username=usernam, password=passwor)
            print(user)
            if user is not None:
                auth.login(request, user)
                print("logged in")
                cus = Customer.objects.get(user_id=request.user.id)
                cus.online_status = 1
                cus.save()
                return redirect('userMS:dashboard')

            else:
                messages.info(request, 'Username or Password is incorrect.')

        return render(request=request, template_name="userMS/login.html", context={})


def register(request):
    if request.user.is_authenticated:
        return redirect('userMS:dashboard')
    else:
        form = CreateUserForm()
        form2 = CreateUserForm2()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            form2 = CreateUserForm2(request.POST)
            if form.is_valid() and form2.is_valid():
                user = form.save()
                user.save()
                profile = form2.save(commit=False)
                profile.user = User.objects.get(pk=user.id)
                profile.save()
                username = user.username
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                cus = Customer.objects.get(user_id=request.user.id)
                cus.online_status = 1
                cus.save()
                return redirect('userMS:dashboard')
        context = {'form': form, 'form2': form2}
        return render(request, 'userMS/register.html', context)


def signout(request):
    cus = Customer.objects.get(user_id=request.user.id)
    cus.online_status = 0
    cus.save()
    logout(request)
    return redirect('userMS:login')


@login_required(login_url='userMS:login')
def dashboard(request):
    return render(request, "userMS/dashboard.html", {"usr": User.objects.get(pk=request.user.id)})


@login_required(login_url='userMS:login')
def dashboard(request):
    return render(request, "userMS/dashboard.html", {"usr": User.objects.get(pk=request.user.id)})


# @login_required(login_url='userMS:login')
# def editProfile(request):
#     if(request.method == "POST"):
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         contact = request.POST['contact']
#         address = request.POST['address']
#         dob = request.POST['dob']
#         gender = request.POST['gender']
#         myfile = request.FILES.get('photo')
#         if myfile.size < 2e+6:
#             return render(request, "userMS/edit-profile.html", context={"err": "Image size limit exceed then 3mb"})
#         usr = User.objects.get(pk=request.user.id)
#         cus = Customer.objects.get(user_id=usr.id)
#         usr.first_name = first_name
#         usr.last_name = last_name
#         usr.save()
#         if(myfile is not None):
#             cus.photo.delete()
#             fs = FileSystemStorage()
#             filename = fs.save(myfile.name, myfile)
#             cus.photo = filename
#         cus.contact = contact
#         cus.address = address
#         cus.dob = dob
#         cus.gender = gender
#         cus.save()
#         return redirect('userMS:dashboard')
#     else:
#         return render(request, "userMS/edit-profile.html", context={})

#     return render(request, "userMS/edit-profile.html", {"usr": User.objects.get(pk=request.user.id)})


@login_required(login_url='userMS:login')
def editProfile(request):
    form = UpdateUserForm(instance=request.user)
    customer = request.user.customer
    form2 = UpdateUserForm2(instance=customer)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        form2 = UpdateUserForm2(request.POST, request.FILES, instance=customer)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect("userMS:dashboard")

    context = {'form': form, 'form2': form2}
    return render(request, "userMS/edit-profile.html", context)


@login_required(login_url='userMS:login')
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('userMS:dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userMS/change-password.html', {
        'form': form
    })
