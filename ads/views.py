import json
import os
import requests
from PIL import Image
from io import BytesIO
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, DeleteView, UpdateView
from DZ27.settings import TOTAL_ON_PAGE
from ads.models import Ad, User
from categories.models import Category


class IndexView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-price')  # Сортировка по убыванию цены

    def get(self, request, *args, **kwargs):
        ads = self.get_queryset()

        paginator = Paginator(ads, per_page=TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        ad_list = [
            {
                'id': ad.id,
                'name': ad.name,
                'author_id': ad.author.id,
                'author': ad.author.username,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'category_id': ad.category.id,
                'image': ad.image.url if ad.image else None
            }
            for ad in page_obj
        ]

        response_data = {
            'items': ad_list,
            'total': paginator.count,
            'num_pages': paginator.num_pages
        }

        return JsonResponse(response_data, status=200)


class AdDetailView(DetailView):
    model = Ad
    queryset = Ad.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        ad = context['object']
        author_json = serialize('json', [ad.author])
        author_data = json.loads(author_json)[0]['fields']
        ad_data = {
            'id': ad.id,
            'name': ad.name,
            'author': author_data,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
        }
        return JsonResponse(ad_data)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', 'image', 'category']

    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body)

        name = request_data.get('name', '')
        price = request_data.get('price', 0.00)
        description = request_data.get('description', '')
        is_published = request_data.get('is_published', False)
        image_url = request_data.get('image', '')
        username = request_data.get('username', '')
        category_id = request_data.get('category_id', None)

        author = User.objects.get(username=username)
        category = Category.objects.get(id=category_id)

        ad = Ad(
            name=name,
            author=author,
            price=price,
            description=description,
            is_published=is_published,
            category=category
        )

        if image_url:
            try:
                response = requests.get(image_url)
                response.raise_for_status()

                image = Image.open(BytesIO(response.content))
                image_temp = BytesIO()
                image.save(image_temp, format=image.format)
                image_temp.seek(0)
                ad.image.save(image_url.split('/')[-1], image_temp, save=True)
            except requests.RequestException as e:
                return JsonResponse({'error': str(e)}, status=500)
            except (IOError, OSError) as e:
                return JsonResponse({'error': 'Ошибка при обработке изображения'}, status=500)

        ad.save()

        response_data = {
            'id': ad.id,
            'name': ad.name,
            'author_id': ad.author.id,
            'author': ad.author.username,
            'price': str(ad.price),
            'description': ad.description,
            'is_published': ad.is_published,
            'category_id': ad.category.id,
            'image': ad.image.url if ad.image else '',
        }

        return JsonResponse(response_data, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'category']

    def patch(self, request, *args, **kwargs):
        ad_id = kwargs['pk']
        ad = self.get_object()

        request_data = json.loads(request.body)

        ad.name = request_data.get('name', ad.name)
        author_id = request_data.get('author_id', None)
        if author_id is not None:
            ad.author_id = author_id

        ad.price = request_data.get('price', ad.price)
        ad.description = request_data.get('description', ad.description)

        category_id = request_data.get('category_id', None)
        if category_id is not None:
            ad.category_id = category_id

        ad.save()

        response_data = {
            'id': ad_id,
            'name': ad.name,
            'author_id': ad.author_id,
            'author': ad.author.username,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'category_id': ad.category_id,
            'image': ad.image.url if ad.image else '',
        }

        return JsonResponse(response_data, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = 'http://localhost/'

    def delete(self, request, *args, **kwargs):
        try:
            ad = self.get_object()

            # Удаление связанной картинки
            if ad.image:
                image_path = ad.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)

            self.object = ad
            success_url = self.get_success_url()
            self.object.delete()

            response_data = {
                'status': 'ok'
            }
            return JsonResponse(response_data, status=200)
        except self.model.DoesNotExist:
            response_data = {
                'error': 'Ad not found.'
            }
            return JsonResponse(response_data, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageAddView(UpdateView):
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        response_data = {
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author.id,
            'author': self.object.author.username,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'category_id': self.object.category.id,
            'image': self.object.image.url if self.object.image else None
        }

        return JsonResponse(response_data, status=200)
