import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView

from ads.models import Ad, Category


class IndexView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):
    def get(self, request):
        ads = Ad.objects.all()
        ad_list = [
            {
                'id': ad.id,
                'name': ad.name,
                'author': ad.author,
                'price': ad.price
            }
            for ad in ads
        ]
        return JsonResponse(ad_list, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)  # Распарсить JSON-данные
            name = data.get('name')  # Получить значение 'name' из данных
            author = data.get('author')  # Получить значение 'author' из данных
            price = data.get('price')  # Получить значение 'price' из данных
            description = data.get('description')  # Получить значение 'description' из данных
            address = data.get('address')  # Получить значение 'address' из данных
            is_published = data.get('is_published')  # Получить значение 'is_published' из данных

            if name and author and price is not None and description and address and is_published is not None:
                ad = Ad.objects.create(
                    name=name,
                    author=author,
                    price=price,
                    description=description,
                    address=address,
                    is_published=is_published
                )
                ad_data = {
                    'id': ad.id,
                    'name': ad.name,
                    'author': ad.author,
                    'price': ad.price,
                    'description': ad.description,
                    'address': ad.address,
                    'is_published': ad.is_published
                }
                return JsonResponse(ad_data)
            else:
                response_data = {
                    'error': 'Invalid form data'
                }
                return JsonResponse(response_data, status=400)
        except json.JSONDecodeError:
            response_data = {
                'error': 'Invalid JSON data'
            }
            return JsonResponse(response_data, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        category_list = [
            {
                'id': category.id,
                'name': category.name,
            }
            for category in categories
        ]
        return JsonResponse(category_list, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)  # Распарсить JSON-данные
            name = data.get('name')  # Получить значение 'name' из данных

            if name:
                category = Category.objects.create(name=name)
                category_data = {
                    'id': category.id,
                    'name': category.name,
                }
                return JsonResponse(category_data)
            else:
                response_data = {
                    'error': 'Invalid form data'
                }
                return JsonResponse(response_data, status=400)
        except json.JSONDecodeError:
            response_data = {
                'error': 'Invalid JSON data'
            }
            return JsonResponse(response_data, status=400)


class CategoryDetailView(DetailView):
    model = Category

    def render_to_response(self, context, **response_kwargs):
        category = context['object']
        category_data = {
            'id': category.id,
            'name': category.name,
        }
        return JsonResponse(category_data)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.kwargs['pk'])
        return obj


class AdDetailView(DetailView):
    model = Ad
    queryset = Ad.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        ad = context['object']
        ad_data = {
            'id': ad.id,
            'name': ad.name,
            'author': ad.author,
            'price': ad.price,
            'description': ad.description,
            'address': ad.address,
            'is_published': ad.is_published,
        }
        return JsonResponse(ad_data)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj
