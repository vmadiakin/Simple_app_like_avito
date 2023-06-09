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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ads.views import IndexView
from users.views import LocationsViewSet, SelectionCreateView, SelectionListView, SelectionDetailView, \
    SelectionUpdateView, SelectionDeleteView

router = routers.SimpleRouter()
router.register('location', LocationsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('ad/', include('ads.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('cat/', include('categories.urls')),
    path('user/', include('users.urls')),
    path('selection/create/', SelectionCreateView.as_view()),
    path('selection/', SelectionListView.as_view()),
    path('selection/<int:pk>/', SelectionDetailView.as_view()),
    path('selection/<int:pk>/update/', SelectionUpdateView.as_view()),
    path('selection/<int:pk>/delete/', SelectionDeleteView.as_view()),
    path('location/<int:pk>/delete/', LocationsViewSet.as_view({'delete': 'destroy'})),
    path('location/<int:pk>/update/', LocationsViewSet.as_view({'patch': 'update'})),
    path('location/create/', LocationsViewSet.as_view({'post': 'create'})),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
