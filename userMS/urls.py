from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views


app_name = "userMS"
urlpatterns = [
    path('login/', views.signIn, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.signout, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/edit-profile/', views.editProfile, name="edit-profile"),
    path('dashboard/change-password/',
         views.changePassword, name="change-password"),

    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name="userMS/reset-password.html"),
         name="password_reset"),

    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="userMS/reset-password-done.html"),
         name="password_reset_done"),

    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="userMS/reset-password-change.html"),
         name="password_reset_confirm"),

    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="userMS/reset-change-done.html"),
         name="password_reset_complete"),

]
