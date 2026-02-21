"""
URL configuration for E_tech_Bazzar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from customer import views

urlpatterns = [
    path("", views.index, name="index"),
    path("base", views.base, name="base"),
    path("Home", views.index, name="Home"),
    path("About", views.About, name="About"),
    path("Contact", views.contact, name="Contact"),
    path("register", views.register, name="register"),
    path("login", views.loginPage, name="login"),
    path("shop", views.shop, name="shop"),
    path("category/<str:slug>", views.category, name="category"),
    path("checkout", views.checkout, name="checkout"),
    path("Wish", views.wish, name="wish"),
    # path('addCart/<str:slug>', views.addCart, name='addCart'),
    path("addCart/", views.addCart, name="addCart"),
    path("search", views.search, name="search"),
    path("logout", views.logoutPage, name="logout"),
    path("fpass", views.forgetpassword, name="fpass"),
    path("payment_process", views.payment_process, name="payment_process"),
    path("success", views.success, name="success"),
    path("Sucess1", views.Sucess1, name="Sucess1"),
    path("ordertrack/<int:slug>", views.ordertrack, name="ordertrack"),
    path("ordertrack/", views.ordertrack, name="ordertrack"),
    path("product/<str:slug>", views.product, name="product"),
    path("userorders", views.userorders, name="userorders"),
    path("orderdetails/<int:slug>", views.orderdetails, name="orderdetails"),
    path("cancelorder/<int:slug>", views.cancelorder, name="cancelorder"),
    path("filter", views.filter, name="filter"),
    path("review", views.review, name="review"),
    path("analysis", views.analysis, name="analysis"),
]
