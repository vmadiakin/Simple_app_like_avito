from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    UserCreateView,
    UserDeleteView,
    UserUpdateView
)

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
]
