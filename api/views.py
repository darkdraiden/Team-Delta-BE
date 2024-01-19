from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializer import *


# Create your views here.
def index(request):
    return HttpResponse("hello")

@api_view(['POST'])
def signin(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if User.objects.filter(email=email, password=password):
        return Response({"Success":"User is authorized"},status=200)
    return Response("Invalid user credentials",status=400)

@api_view(['POST'])
def signup(request):
    data = request.data
    serializer = UserSerializer(data=data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Sucess":"User created successfully"},status=201)
    else:
        return Response(serializer.errors,status=400)