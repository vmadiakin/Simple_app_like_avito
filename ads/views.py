from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from ads.models import Ad
from ads.serializers import AdSerializer, UploadImageSerializer


class IndexView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"})


class AdsViewSet(ModelViewSet):
    queryset = Ad.objects.all().order_by('-price')
    serializer_class = AdSerializer
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        ad = self.get_object()
        serializer = UploadImageSerializer(ad, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('cat')
        if category_id:
            queryset = queryset.filter(Q(category_id=category_id) | Q(category_id__isnull=True))
        search_text = self.request.query_params.get('text')
        if search_text:
            queryset = queryset.filter(name__icontains=search_text)
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(author__location__name__icontains=location)
        price_from = self.request.query_params.get('price_from')
        price_to = self.request.query_params.get('price_to')
        if price_from and price_to:
            queryset = queryset.filter(price__range=(price_from, price_to))
        return queryset
