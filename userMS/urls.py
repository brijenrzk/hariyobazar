from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import line_chart, line_chart_json
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
    path('dashboard/verify-email', views.verifyEmail, name="verify-email"),
    path('dashboard/change-email', views.changeEmail, name="change-email"),

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


    # admin urls
    path('admin-dashboard/', views.adminDashboard, name="admin-dashboard"),
    path('admin-dashboard/profile', views.adminProfile, name="admin-profile"),
    path('admin-dashboard/edit-profile',
         views.adminEditProfile, name="admin-edit-profile"),
    path('admin-dashboard/change-password',
         views.adminChangePassword, name="admin-change-password"),
    path('admin-dashboard/add-user', views.adminAddUser, name="admin-add-user"),
    path('admin-dashboard/users-list',
         views.adminUsersList, name="admin-users-list"),
    path('admin-dashboard/user/<int:pk>/',
         views.adminUser, name="admin-user"),
    path('admin-dashboard/user-delete/<int:pk>/',
         views.adminUserDelete, name="admin-user-delete"),
    path('admin-dashboard/user-block/<int:pk>/',
         views.adminUserBlock, name="admin-user-block"),

    path('chart/', line_chart, name='line_chart'),
    path('chartJSON/', line_chart_json, name='line_chart_json'),

]
