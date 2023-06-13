from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from ads.models import Ad
from ads.serializers import AdListSerializer
from users.models import User, Location, Selection


class UserListSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField(source='location.name')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'role', 'location']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserDetailSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField(source='location.name')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'role', 'location']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'role', 'location', 'birth_date', 'email']

    def get_location(self, obj):
        location_name = obj.location.name if obj.location else None
        return location_name

    def create(self, validated_data):
        location_data = self.initial_data.get('location')
        location_name = location_data[0] + ', ' + location_data[1]
        location_lat = None
        location_lng = None

        if len(location_data) >= 3:
            location_lat = location_data[2]

        if len(location_data) >= 4:
            location_lng = location_data[3]

        location_obj, _ = Location.objects.get_or_create(name=location_name, lat=location_lat, lng=location_lng)

        validated_data['location'] = location_obj
        validated_data['password'] = make_password(validated_data['password'])

        user = User.objects.create(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'role', 'location']
        read_only_fields = ['id']  # Чтобы идентификатор пользователя был только для чтения

    def get_location(self, obj):
        location_name = obj.location.name if obj.location else None
        return location_name

    def update(self, instance, validated_data):
        location_data = self.initial_data.get('location')

        if location_data:
            location_name = location_data[0] + ', ' + location_data[1]
            location_lat = None
            location_lng = None

            if len(location_data) >= 3:
                location_lat = location_data[2]

            if len(location_data) >= 4:
                location_lng = location_data[3]

            location_obj, _ = Location.objects.get_or_create(name=location_name, lat=location_lat, lng=location_lng)
            instance.location = location_obj

        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.age = validated_data.get('age', instance.age)

        instance.save()
        return instance


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        many=True
    )

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdListSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionUpdateSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        many=True
    )

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id']
