from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from productMS.views import PremiumView, LatestView, CategoryView

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
    path('sell', views.sell, name="sell"),
    path('my-ads', views.myAds, name="myAds"),
    path('my-ads/delete/<int:pk>', views.deleteMyAds, name="deleteMyAds"),
    path('my-ads/edit/<int:pk>', views.postEditProducts, name="editMyAds"),
    path('fav', views.favourite_add, name="favourite_add"),

    path('comments', views.comments, name="comments"),
    path('comments/reply/<int:pk>', views.reply, name="reply"),
    path('premium-products', PremiumView.as_view(), name="premium-products"),
    path('latest-products', LatestView.as_view(), name="latest-products"),
    path('category/<slug:slug>/', CategoryView.as_view(), name="category-products"),
    path('search', views.searchProduct, name="search-products"),
    path('product/<slug:slug>/', views.singleProduct, name="single-product"),
]
