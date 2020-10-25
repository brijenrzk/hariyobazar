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
from .models import Customer, EmailVerification
from .forms import CreateUserForm, CreateUserForm2, UpdateUserForm, UpdateUserForm2
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from random import randint
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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
                cus = Customer.objects.get(user_id=request.user.id)
                cus.online_status = 1
                cus.save()
                # print()
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
                em = EmailVerification(user=user)
                em.save()
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
            messages.success(
                request, 'Your profile was successfully updated!')
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
        form = PasswordChangeForm(request.user)
    return render(request, 'userMS/change-password.html', {
        'form': form
    })


def changeEmail(request):
    em = EmailVerification.objects.get(user=request.user)
    if request.method == 'POST':
        email = request.POST['email']
        checkExist = User.objects.filter(email=email)
        if not checkExist:
            usr = request.user
            usr.email = email
            usr.save()
            em.verify_status = 0
            em.save()
            messages.success(request, 'Your email was successfully changed!')
            return redirect('userMS:dashboard')
        else:
            messages.info(request, 'This email already exists')
    return render(request, "userMS/change-email.html", {})


@login_required(login_url='userMS:login')
def verifyEmail(request):
    em = EmailVerification.objects.get(user=request.user)
    if em.verify_status:
        return redirect('userMS:dashboard')
    if request.method == 'POST':
        code = request.POST['code']
        if code == str(em.verify_code):
            em.verify_status = 1
            em.save()
            messages.success(
                request, 'Your email was successfully verified!')
            return redirect('userMS:dashboard')
        else:
            messages.info(request, 'Code does not match.')

    else:
        val = randint(100000, 999999)
        em.verify_code = val
        em.verify_status = 0
        em.save()
        template = render_to_string(
            'userMS/email-template.html', {'name': request.user.first_name, 'code': em.verify_code})
        email = EmailMessage('Confirm your email address',
                             template, settings.EMAIL_HOST_USER, [request.user.email],)
        email.fail_silently = False
        email.send()

    return render(request, "userMS/verify-email.html", {})
