import json
import jwt
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers
from django.db import connection
from .autentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
import environ
from .models import User, Client as ClientModel, Product as ProductModel, Bill as BillModel, BillProduct
env = environ.Env()
base = environ.Path(__file__) - 2
environ.Env.read_env(env_file=base('.env'))


class Users(APIView):

    serializer_class = serializers.UserSerializer

    def get(self, req):

        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        print(serializer.data)
        return Response(serializer.data)

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
            user = get_object_or_404(
                User, username=username, password=password)
        except User.DoesNotExist:
            return Response({'Error': "Invalid username/password"}, status="400")
        if user:
            payload = {'id': user.id, 'username': user.username}
            token = jwt.encode(payload, env("SECRET_KEY"))
            print(token)
            jwt_token = {'token': token.decode("utf-8")}
            # User.objects.raw("update user set is_active = true, token= '%s' where id = %s" %(jwt['token'], user['id']))
            c = connection.cursor()
            print(user.id, jwt_token['token'])
            try:
                c.execute("UPDATE public.user SET (is_active, token) = ('true','%s') WHERE id=%s RETURNING *;" %
                          (jwt_token['token'], user.id))
                result = c.fetchone()
                print(result)
                return Response(jwt_token, status=200)
            except Exception as e:
                print(e)
                return Response({'error': str(e)}, status=500)
            finally:
                c.close()
        else:
            return Response({'Error': "Invalid credentials"}, status=400)


class ClientDetail(APIView):

    serializer_class = serializers.ClientSerializer

    def get(self, req, clientId):

        client = get_object_or_404(ClientModel, pk=clientId)
        serializer = self.serializer_class(client)
        print(serializer.data)
        return Response(serializer.data)


class Client(APIView):

    serializer_class = serializers.ClientSerializer

    def get(self, req):

        clients = ClientModel.objects.all()
        serializer = self.serializer_class(clients, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, req):
        data = req.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, req, clientId):

        qs = get_object_or_404(ClientModel, pk=clientId)
        qs.delete()
        return Response(status=204)

class Bill(APIView):

    serializer_class = serializers.BillSerializer

    def post(self, req, clientId):
        data = req.data
        data['client'] = clientId
        print(data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def delete(self, req, billId):

        qs = get_object_or_404(BillModel, pk=billId)
        qs.delete()
        return Response(status=204)


class Product(APIView):

    serializer_class = serializers.ProductSerializer

    def post(self, req, billId):
        data = req.data
        data['bill'] = billId
        print(data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, req):
        data = req.data
        print(data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, req, productId):

        qs = get_object_or_404(ProductModel, pk=productId)
        qs.delete()
        return Response(status=204)


class ClientExport(APIView):

    def get(self, req, clientId):

        c = connection.cursor()
        try:
            c.execute("SELECT c.document, CONCAT(c.first_name, ' ', c.last_name) as fullname, COUNT(bill.client_id) as number from client c inner join bill on (c.id = bill.client_id) group by c.document, fullname")
            result = c.fetchone()
            print(result)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="facturas.csv"'
            writer = csv.writer(response)

            writer.writerow(
                ['Documento', 'Nombre completo', 'Cantidad de facturas'])
            writer.writerow(result)
            return response
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=500)
        finally:
            c.close()
