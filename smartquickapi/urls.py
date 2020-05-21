"""smartquick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from smartquickapi import views
from rest_framework import routers


urlpatterns = [
    path('users', views.Users.as_view()),
    # path('users/<str:userId>', views.Users.as_view()),
    path('login', views.Login.as_view()),

    path('clients', views.Client.as_view()),
    path('clients/<str:clientId>', views.ClientDetail.as_view()),
    path('clients/<str:clientId>/bill', views.Bill.as_view()),
    path('bills/<str:billId>/products', views.Product.as_view()),
    path('products', views.Product.as_view()),
    path('products/<str:productId>', views.Product.as_view()),

    path('clients/<str:clientId>/exports', views.ClientExport.as_view()),
]
