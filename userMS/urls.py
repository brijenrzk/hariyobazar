from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = "userMS"
urlpatterns = [
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.signout, name="logout"),
]
