# # artist_api/serializers.py
# from django.contrib.auth.models import User
# from rest_framework import serializers
# from .models import Work, Artist, WorkType

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'password']  # Add any additional fields you want to include

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user

# class WorkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Work
#         fields = ['link', 'work_type']

# class ArtistSerializer(serializers.ModelSerializer):
#     works = WorkSerializer(many=True, read_only=True)

#     class Meta:
#         model = Artist
#         fields = ['id', 'name', 'user', 'works']


# class WorkTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WorkType
#         fields = ['name', 'value']


# class ArtistDetailSerializer(serializers.ModelSerializer):
#     works = WorkSerializer(many=True, read_only=True)
#     user = serializers.ReadOnlyField(source='user.username')

#     class Meta:
#         model = Artist
#         fields = ['id', 'name', 'user', 'works']

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Artist, Work

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ['link', 'work_type']

class ArtistSerializer(serializers.ModelSerializer):
    works = WorkSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ['id', 'name', 'user', 'works']
