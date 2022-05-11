"""Lexcovery_Sanctions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_view, name='main_view'),
    path('search/', views.search, name='search_view'),
    path('support/', views.support, name='support_view'),
    path('donate/', views.donate, name='donate_view'),
    path('sources/', views.sources, name='sources_view'),
    path('upload/', views.upload, name='upload_view')
]