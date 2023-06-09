from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from ads.models import Ad
from ads.permissions import IsAuthorOrModeratorOrAdmin
from ads.serializers import AdListSerializer, AdDetailSerializer, AdCreateSerializer, AdUpdateSerializer, \
    UploadImageSerializer, AdDestroySerializer


class IndexView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"})


class AdsListView(ListAPIView):
    queryset = Ad.objects.all().order_by('-price')
    serializer_class = AdListSerializer

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


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrModeratorOrAdmin]


class AdUploadImageView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = UploadImageSerializer


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer
    permission_classes = [IsAuthenticated, IsAuthorOrModeratorOrAdmin]
