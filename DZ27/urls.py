"""
URL configuration for DZ27 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from ads.views import IndexView, CategoryView, CategoryDetailView, AdView, AdDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('ad/', AdView.as_view(), name='ad-list'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    path('cat/', CategoryView.as_view(), name='category-list'),
    path('cat/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]
