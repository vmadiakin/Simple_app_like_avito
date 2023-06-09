from rest_framework import serializers
from ads.models import Ad
from categories.models import Category
from users.models import User


class AdListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')
    category = serializers.StringRelatedField(source='category.name')

    class Meta:
        model = Ad
        fields = "__all__"


class AdDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')
    category = serializers.StringRelatedField(source='category.name')

    class Meta:
        model = Ad
        fields = "__all__"


class AdCreateSerializer(serializers.ModelSerializer):
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
    author = serializers.StringRelatedField(source='author.username')
    category = serializers.StringRelatedField(source='category.name')
    image = serializers.ImageField(required=False)

    class Meta:
        model = Ad
        fields = "__all__"


class AdUpdateSerializer(serializers.ModelSerializer):
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
    author = serializers.StringRelatedField(source='author.username')
    category = serializers.StringRelatedField(source='category.name')
    image = serializers.ImageField(required=False)

    class Meta:
        model = Ad
        fields = "__all__"


class UploadImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = Ad
        fields = ['image']


class AdDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id']
