import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Ad
from .models import User, Location


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('username')

    def render_to_response(self, context, **response_kwargs):
        data = {
            'items': [],
            'total': context['object_list'].count(),
            'num_pages': 1
        }
        for user in context['object_list']:
            locations = [user.location.name]
            data['items'].append({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'age': user.age,
                'locations': locations
            })
        return JsonResponse(data, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        # Получение количества опубликованных объявлений пользователя
        total_ads = Ad.objects.filter(author=user, is_published=True).count()

        data = {
            'items': [
                {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'age': user.age,
                    'location': user.location.name if user.location else None,
                    'total_ads': total_ads,
                }
            ]
        }

        return JsonResponse(data, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age']

    def create_location(self, location_name):
        parts = location_name.split(', ')
        name = parts[0]
        if len(parts) > 1 and parts[1].startswith('м.'):
            name += ', ' + parts[1]
        location, created = Location.objects.get_or_create(name=name, lat=0, lng=0)
        return location

    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body)

        username = request_data.get('username', '')
        password = request_data.get('password', '')
        first_name = request_data.get('first_name', '')
        last_name = request_data.get('last_name', '')
        role = request_data.get('role', '')
        age = request_data.get('age', 0)
        locations = request_data.get('locations', [])

        location_name = ', '.join(locations)

        location = self.create_location(location_name)

        user = User(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            age=age,
            location=location
        )
        user.save()

        response_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'location': user.location.name
        }

        return JsonResponse(response_data, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'age', 'location', 'lat', 'lng']

    def patch(self, request, *args, **kwargs):
        user_id = kwargs['pk']
        user = self.get_object()

        request_data = json.loads(request.body)

        user.username = request_data.get('username', user.username)
        user.password = request_data.get('password', user.password)
        user.first_name = request_data.get('first_name', user.first_name)
        user.last_name = request_data.get('last_name', user.last_name)
        user.age = request_data.get('age', user.age)
        location_name = request_data.get('location', user.location.name)
        lat = request_data.get('lat', user.location.lat)
        lng = request_data.get('lng', user.location.lng)
        location, _ = Location.objects.get_or_create(name=location_name, lat=lat, lng=lng)
        user.location = location

        user.save()

        response_data = {
            'id': user_id,
            'username': user.username,
            'password': user.password,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'location': user.location.name,
            'lat': user.location.lat,
            'lng': user.location.lng,
        }

        return JsonResponse(response_data, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = 'http://localhost/'

    def delete(self, request, *args, **kwargs):
        try:
            user = self.get_object()

            self.object = user
            success_url = self.get_success_url()
            self.object.delete()

            response_data = {
                'status': 'ok'
            }
            return JsonResponse(response_data, status=200)
        except self.model.DoesNotExist:
            response_data = {
                'error': 'User not found.'
            }
            return JsonResponse(response_data, status=404)
