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
from productMS.models import Product
from .forms import CreateUserForm, CreateUserForm2, UpdateUserForm, UpdateUserForm2, UpdateAdminForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from random import randint
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .decorators import admin_only, user_only
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.urls import reverse
from django.db.models import Count
from django.db.models.functions import TruncDay
from productMS.models import Questions

# Create your views here.


def signIn(request):
    if request.user.is_authenticated:
        return redirect('userMS:dashboard')
    else:
        if request.method == 'POST':
            usernam = request.POST['username']
            try:
                username = User.objects.get(email=usernam).username
            except User.DoesNotExist:
                username = request.POST['username']
            passwor = request.POST['password']
            user = authenticate(request, username=username, password=passwor)
            if user is not None:
                auth.login(request, user)
                if not user.is_superuser:
                    cus = Customer.objects.get(user_id=request.user.id)
                    cus.online_status = 1
                    cus.save()
                # print()
                return redirect('productMS:index')
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
    if not request.user.is_superuser:
        cus = Customer.objects.get(user_id=request.user.id)
        cus.online_status = 0
        cus.save()
    logout(request)
    return redirect('userMS:login')


@user_only
@login_required(login_url='userMS:login')
def dashboard(request):
    cmt = Questions.objects.filter(
        answer__exact='').count()
    return render(request, "userMS/dashboard.html", {"usr": User.objects.get(pk=request.user.id), 'cmt': cmt})


@user_only
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


@user_only
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


@user_only
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


@user_only
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


# All admin functions

@admin_only
@login_required(login_url='userMS:login')
def adminDashboard(request):
    cus1 = Customer.objects.all()
    cus = Customer.objects.filter(online_status=1).exclude(user=request.user)
    prod = Product.objects.all()
    total_customer = cus1.count()
    total_online = cus.count()
    total_prod = prod.count()
    return render(request, 'userMS/admin/dashboard.html', {"total_customer": total_customer, "total_online": total_online, "total_prod": total_prod})


@admin_only
@login_required(login_url='userMS:login')
def adminProfile(request):
    return render(request, "userMS/admin/admin-profile.html", {"usr": User.objects.get(pk=request.user.id)})


@admin_only
@login_required(login_url='userMS:login')
def adminEditProfile(request):
    form = UpdateAdminForm(instance=request.user)
    if request.method == 'POST':
        form = UpdateAdminForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your profile was successfully updated!')
            return redirect("userMS:admin-profile")

    context = {'form': form}
    return render(request, "userMS/admin/admin-edit.html", context)


@admin_only
@login_required(login_url='userMS:login')
def adminChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('userMS:admin-profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userMS/admin/admin-update-pass.html', {
        'form': form
    })


@admin_only
@login_required(login_url='userMS:login')
def adminAddUser(request):
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
            messages.success(request, 'User added successfully')
            return redirect('userMS:admin-users-list')
    context = {'form': form, 'form2': form2}
    return render(request, 'userMS/admin/admin-add-user.html', context)


class LineChartJSONView(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""

        return ["Day-1", "Day-2", "Day-3", "Day-4", "Day-5", "Day-6", "Day-7"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Registered User"]

    def get_data(self):
        """Return 3 datasets to plot."""
        total_users_online = []
        start_date = timezone.now() - timedelta(days=7)
        end_date = timezone.now()
        delta = timedelta(days=1)
        newEnd = timezone.now() - timedelta(days=6)
        while start_date < end_date-delta:
            usr = User.objects.filter(date_joined__range=(start_date, newEnd)).annotate(day=TruncDay('date_joined')).values(
                'day').values_list('date_joined', flat=True)
            total_users_online.append(len(usr))
            newEnd += delta
            start_date += delta
        return [total_users_online]


line_chart = TemplateView.as_view(template_name='userMS/admin/dashboard.html')
line_chart_json = LineChartJSONView.as_view()


@admin_only
@login_required(login_url='userMS:login')
def adminUsersList(request):
    usr = User.objects.all().exclude(id=request.user.id)
    cus = Customer.objects.all()
    context = {"usr": usr, "cus": cus}
    return render(request, "userMS/admin/admin-user-list.html", context)


@admin_only
@login_required(login_url='userMS:login')
def adminUser(request, pk=None):
    return render(request, "userMS/admin/admin-user.html", {"user": User.objects.get(pk=pk)})


@admin_only
@login_required(login_url='userMS:login')
def adminUserDelete(request, pk=None):
    u = User.objects.get(id=pk)
    u.delete()
    messages.success(request, 'User Deleted')
    return redirect('userMS:admin-users-list')


@admin_only
@login_required(login_url='userMS:login')
def adminUserBlock(request, pk=None):
    u = User.objects.get(id=pk)
    if u.is_active:
        u.is_active = False
        u.save()
        messages.success(request, 'User Blocked')
        return redirect('userMS:admin-users-list')
    else:
        u.is_active = True
        u.save()
        messages.success(request, 'User Unblocked')
        return redirect('userMS:admin-users-list')
