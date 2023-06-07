from rest_framework import serializers
from ads.models import Ad
from categories.models import Category
from users.models import User


class AdSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    image = serializers.ImageField(required=False)
    author_name = serializers.StringRelatedField(source='author.username')
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    category_name = serializers.StringRelatedField(source='category.name')

    class Meta:
        model = Ad
        fields = ['id', 'name', 'author_id', 'author_name', 'author_first_name', 'price', 'description', 'is_published', 'image', 'category_id', 'category_name']

    def create(self, validated_data):
        return super().create(validated_data)


class UploadImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = Ad
        fields = ['image']
