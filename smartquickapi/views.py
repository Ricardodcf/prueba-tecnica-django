import json
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers
from django.db import connection
import environ
from .models import User, Client
env = environ.Env()
base = environ.Path(__file__) - 2
environ.Env.read_env(env_file=base('.env'))


class Prueba(APIView):

    def get(self, req):
        print('llego aqui!')
        return Response({'success': True}, 201)


class Users(APIView):

    serializer_class = serializers.UserSerializer

    def get(self, req, userId):

        return Response({'success': True, 'user': userId}, 201)
        # return Response({})

    def post(self, req):

        data = req.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class Login(TokenObtainPairView):

    serializer_class = serializers.UserSerializer

    def post(self, req):
        if not req.data:
            return Response({'Error': "Please provide username/password"}, status="400")

        username = req.data['username']
        password = req.data['password']
        try:
            user = get_object_or_404(User, username=username, password=password)
        except User.DoesNotExist:
            return Response({'Error': "Invalid username/password"}, status="400")
        if user:
            payload = {'id': user.id, 'username': user.username}
            jwt_token = {'token': jwt.encode(payload, env("SECRET_KEY"))}
            User.objects.raw("update user set is_active = true, token= %s where id = %s" %(jwt['token'], user['id']))
            # serializer = self.serializer_class(
            #     user, data=jwt_token, partial=True)
            # if serializer.is_valid():
            #     serializer.save()
            return Response(jwt_token, status=200)
            # else:
            #     return Response(serializer.errors, status=400)

        else:
            return Response({'Error': "Invalid credentials"}, status=400)


# class Client(APIView):
    # permission_classes = (IsAuthenticated,)
#     def get(self, req):
