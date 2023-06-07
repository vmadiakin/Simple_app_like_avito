from django.urls import path

from ads.views import AdsViewSet

urlpatterns = [
    path('create/', AdsViewSet.as_view({'post': 'create'})),
    path('<int:pk>/delete/', AdsViewSet.as_view({'delete': 'destroy'})),
    path('<int:pk>/update/', AdsViewSet.as_view({'patch': 'update'})),
    path('<int:pk>/upload_image/', AdsViewSet.as_view({'post': 'upload_image'}), name='ad-upload-image'),
]
