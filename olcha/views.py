from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status,viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BaseAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from olcha.models import Category,Group,Product,Comment
from olcha.serializers import ProductModelSerializer,CommentModelSerializer,CategoryModelSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication



# Create your views here.

"""  1 st  and 2 nd version  Barcha ma'lumotlarni bitta viewda chiqarish uchun """

# class CategoryList(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryModelSerializer
#     permission_classes = [AllowAny]


class CategoryListView(APIView):
    def get(self,request):
        categories = Category.objects.all()
        serializers = CategoryModelSerializer(categories, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)
    

class ProductListView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializers = ProductModelSerializer(products,many=True,context = {'request':request})
        return Response(serializers.data,status=status.HTTP_200_OK)


class CommentListView(APIView):
    def get(self,request):
        comments = Comment.objects.all()
        serializers = CommentModelSerializer(comments,many = True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class UserListView(APIView):
    def get(self,request):
        users = User.objects.all()
        serializers = UserModelSerializer(users,many=True,context = {'request':request})
        return Response(serializers.data,status = status.HTTP_200_OK)



class register(APIView):
    def post(self,request,format = None):
        serializer = UserRegister(data = request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'registered'
            data['username'] = account.username
            data['email'] = account.email
            token,create  = Token.objects.get_or_create(user =account)
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data)
  





class CategoryList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()

    


class CategoryDetail(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    lookup_field = 'pk'

    # def get_queryset(self):
    #     queryset = Category.objects.all()
    #     return queryset


class CategoryAdd(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()


class CategoryDelete(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()

class CategoryListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()

class CategoryChange(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()


class CategoryModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()

#  For Product section

class ProductList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()


class ProductAdd(generics.CreateAPIView):
    
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()


class ProductDelete(generics.DestroyAPIView):
    
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()

class ProductListCreate(generics.ListCreateAPIView):
    
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()

class ProductChange(generics.UpdateAPIView):
    
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()


class ProductModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()