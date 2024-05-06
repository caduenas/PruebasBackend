from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class HashingSerializer(serializers.Serializer):
    cadena = serializers.CharField()
    hashmethod = serializers.CharField()