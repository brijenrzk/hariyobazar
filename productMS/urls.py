from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views


app_name = "productMS"

urlpatterns = [
    path('admin-dashboard/products',views.adminProductsList, name="admin-products-list"),
    path('admin-dashboard/products/add',views.adminProductsAdd, name="admin-products-add"),
    path('admin-dashboard/category',views.adminProductsCategory, name="admin-products-category"),
    path('admin-dashboard/category/add',views.adminProductsAddCategory, name="admin-products-add-category"),
    path('admin-dashboard/category/delete/<int:pk>/',views.adminProductsDeleteCategory, name="admin-products-delete-category"),
    path('admin-dashboard/category/edit/<int:pk>/',views.adminProductsEditCategory, name="admin-products-edit-category"),

    path('admin-dashboard/sub-category',views.adminProductsSubCategory, name="admin-products-subcategory"),
    path('admin-dashboard/sub-category/add',views.adminProductsAddSubCategory, name="admin-products-add-subcategory"),
    path('admin-dashboard/sub-category/delete/<int:pk>/',views.adminProductsDeleteSubCategory, name="admin-products-delete-subcategory"),
    path('admin-dashboard/sub-category/edit/<int:pk>/',views.adminProductsEditSubCategory, name="admin-products-edit-subcategory"),
]
