from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import User, Location, Selection
from .permissions import IsOwnerOrReadOnly
from .serializers import UserListSerializer, UserDetailSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserDestroySerializer, LocationSerializer, SelectionCreateSerializer, SelectionListSerializer, \
    SelectionDetailSerializer, SelectionUpdateSerializer, SelectionDeleteSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer


class LocationsViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDeleteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
