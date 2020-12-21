from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views


app_name = "productMS"

urlpatterns = [
    path('admin-dashboard/products/all',
         views.adminProductsAll, name="admin-products-all"),
    path('admin-dashboard/products', views.adminProductsList,
         name="admin-products-list"),
    path('admin-dashboard/products/add',
         views.adminProductsAdd, name="admin-products-add"),
    path('admin-dashboard/products/delete/<int:pk>/',
         views.adminProductsDelete, name="admin-products-delete"),
    path('admin-dashboard/products/edit/<int:pk>/',
         views.adminProductsEdit, name="admin-products-edit"),
    path('admin-dashboard/category', views.adminProductsCategory,
         name="admin-products-category"),
    path('admin-dashboard/category/add', views.adminProductsAddCategory,
         name="admin-products-add-category"),
    path('admin-dashboard/category/delete/<int:pk>/',
         views.adminProductsDeleteCategory, name="admin-products-delete-category"),
    path('admin-dashboard/category/edit/<int:pk>/',
         views.adminProductsEditCategory, name="admin-products-edit-category"),

    path('admin-dashboard/sub-category', views.adminProductsSubCategory,
         name="admin-products-subcategory"),
    path('admin-dashboard/sub-category/add', views.adminProductsAddSubCategory,
         name="admin-products-add-subcategory"),
    path('admin-dashboard/sub-category/delete/<int:pk>/',
         views.adminProductsDeleteSubCategory, name="admin-products-delete-subcategory"),
    path('admin-dashboard/sub-category/edit/<int:pk>/',
         views.adminProductsEditSubCategory, name="admin-products-edit-subcategory"),


    path('ajax/load-subcat/', views.load_subcat,
         name='ajax_load_subcat'),  # AJAX


    # Banner
    path('admin-dashboard/banner', views.adminBanner, name="admin-banner"),
    path('admin-dashboard/banner/add',
         views.adminBannerAdd, name="admin-banner-add"),
    path('admin-dashboard/banner/delete/<int:pk>/',
         views.adminBannerDelete, name="admin-banner-delete"),



    # User side

    path('', views.index, name="index"),
    path('premium-products', views.premiumProducts, name="premium-products"),
    path('latest-products', views.latestProducts, name="latest-products"),
    path('category/<slug:slug>/', views.categoryProducts, name="category-products")
]
