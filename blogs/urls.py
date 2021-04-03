from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from blogs.views import BlogsView

from . import views


app_name = "blogs"


urlpatterns = [

    #path('blogs', views.blogs, name="blog"),
    path('blogs', BlogsView.as_view(), name="blog"),
    path('blogs/<slug:slug>', views.singleBlog, name="single-blog"),


    # admin
    path('admin-dashboard/blogs', views.adminBlogs, name="admin-blogs"),
    path('admin-dashboard/blogs/add', views.adminAddBlogs, name="admin-blogs-add"),
    path('admin-dashboard/blogs/delete/<int:pk>',
         views.adminDeleteBlogs, name="admin-blogs-delete"),
    path('admin-dashboard/blogs/edit/<slug:slug>',
         views.adminEditBlogs, name="admin-blogs-edit"),

]
