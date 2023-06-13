from django.urls import path

from ads.views import AdsListView, AdDetailView, AdCreateView, AdUpdateView, AdUploadImageView, AdDeleteView
urlpatterns = [
    path('', AdsListView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('create/', AdCreateView.as_view()),
    path('<int:pk>/delete/', AdDeleteView.as_view()),
    path('<int:pk>/update/', AdUpdateView.as_view()),
    path('<int:pk>/upload_image/', AdUploadImageView.as_view()),
]
