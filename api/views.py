from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
@api_view(['POST'])
def signup(request):
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Sucess":"User created successfully"},status=201)
    else:
        return Response(serializer.errors,status=400)

@api_view(['GET'])
def travelplan(request):
    data = TravelPlan.objects.all()
    serializer = TravelPlanSerializer(data,many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def settravelplan(request):
    data = request.data
    serializer = TravelPlanSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Sucess":"Travel Plan created successfully"},status=201)
    else:
        return Response(serializer.errors,status=400)

@csrf_exempt
@api_view(['PUT'])
def updatetravelplan(request):
    travel_id = request.data.get('travel_id')
    try:
        title = request.data.get('title')
        location = request.data.get('location')
        rate = request.data.get('rate')
        start_date = request.data.get('start_date')
        about = request.data.get('about')
        TPlan = TravelPlan.objects.get(travel_id=travel_id)
        if title:
            TPlan.title = title
        if location:
            TPlan.location = location
        if rate:
            TPlan.rate = rate
        if start_date:
            TPlan.start_date = start_date
        if about:
            TPlan.about = about
        TPlan.save()
        return Response({"Success":"Travel Plan successfully updated"},status=200)
    except models.TravelPlan.DoesNotExist:
        return Response({"Failed":"No Travel Plan found"},status=400)
    
@csrf_exempt
@api_view(['DELETE'])
def deletetravelplan(request,travel_id):
    try:
        TPlan = TravelPlan.objects.get(travel_id=travel_id)
        TPlan.delete()
        return Response("Travel Plan deleted successfully",status=200)
    except models.TravelPlan.DoesNotExist:
        return Response({"Failed":"No Travel Plan found"},status=400)


@api_view(['GET'])
def getbooking(request):
    data = Booking.objects.all()
    serializer = BookingSerializer(data,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def getbookingof(request):
    user_id = request.data.get('user_id')
    bookings=Booking.objects.filter(user_id=user_id)
    data = []
    count = 0
    for i in bookings:
        travel_id = BookingSerializer(i).data.get('travel')
        member_count = BookingSerializer(i).data.get('member_count')
        booking_price = BookingSerializer(i).data.get('booking_price')
        data.append(TravelPlanSerializer(TravelPlan.objects.get(travel_id=travel_id)).data)
        data[count].update({'member_count':member_count})
        data[count].update({'booking_price':booking_price})
        count +=1
    return Response(data)

@csrf_exempt
@api_view(['POST'])
def booking(request):
    data = request.data
    serializer = BookingSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Sucess":"Booked successfully"},status=201)
    else:
        return Response(serializer.errors,status=400)

@csrf_exempt
@api_view(['PUT'])
def updatebooking(request):
    booking_id = request.data.get('booking_id')
    try:
        book = Booking.objects.get(booking_id=booking_id)
        booking_price = request.data.get('booking_price')
        travel_id = request.data.get('travel_id')
        user_id  = request.data.get('user_id')
        member_count = request.data.get('member_count')
        if booking_price:
            book.booking_price = booking_price
        if travel_id:
            book.travel_id = travel_id
        if user_id:
            book.user_id = user_id
        if member_count:
            book.member_count = member_count
        book.save()
        return Response({"Success":"Booking successfully updated"},status=200)
    except models.Booking.DoesNotExist:
        return Response({"Failed":"No Booking found"},status=400)

@csrf_exempt
@api_view(['DELETE'])
def deletebooking(request,booking_id):
    try:
        book = Booking.objects.get(booking_id=booking_id)
        book.delete()
        return Response("Booking deleted successfully",status=200)
    except models.Booking.DoesNotExist:
        return Response({"Failed":"Booking not found"},status=400)