from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import HashingSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import hashlib
# Create your views here.

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"error":"Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    token, create = Token.objects.get_or_create(user=user) 
    return Response({"token": token.key}, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(email= email)
            return Response({'error':'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = serializer.save()
            user.set_password(serializer.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def profile(request):
    return Response({})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def hashing(request):
    data = request.data
    serializer = HashingSerializer(data=data)
    if serializer.is_valid():
        cadena = serializer.validated_data['cadena']
        hashmethod = serializer.validated_data['hashmethod']
        hash_hex = ''
        if hashmethod == 'SHA-256':
            hash_object = hashlib.sha256()
        elif hashmethod == 'SHA-1':
            hash_object = hashlib.sha1()
        elif hashmethod == 'SHA-384':
            hash_object = hashlib.sha384()
        elif hashmethod == 'SHA-512':
            hash_object = hashlib.sha512()
        elif hashmethod == 'MD5':
            hash_object = hashlib.md5()
        else:
            return Response({'error': 'Método de hash no válido'}, status=status.HTTP_400_BAD_REQUEST)

        hash_object.update(cadena.encode())
        hash_hex = hash_object.hexdigest()

        return Response({'hash': hash_hex})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
