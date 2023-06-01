from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView

from categories.models import Category


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.order_by('name')  # Сортировка по полю name

    def get(self, request, *args, **kwargs):
        categories = self.get_queryset()
        category_list = [
            {
                'id': category.id,
                'name': category.name,
            }
            for category in categories
        ]
        return JsonResponse(category_list, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body)
        name = form_data.get('name')

        if name:
            category = self.model.objects.create(name=name)
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


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        category = self.get_object()
        form_data = json.loads(request.body)
        name = form_data.get('name')

        if name:
            category.name = name
            category.save()
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


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()

        response_data = {
            'status': 'ok'
        }
        return JsonResponse(response_data)
