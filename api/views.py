from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializer import *
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import default_storage



# Create your views here.
def index(request):
    return HttpResponse("hello")

@csrf_exempt
@api_view(['POST'])
def signin(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response("Invalid user credentials", status=400)

    if check_password(password, user.password):
        request.session['email']=email
        request.session.create()
        session_key = request.session.session_key
        if User.objects.filter(email=email,role="ADMIN"):
            return Response({"sessionid":session_key,"role":"ADMIN"},status=200)
        else:
            return Response({"sessionid":session_key,"role":"USER"},status=200)
    return Response("Invalid user credentials",status=400)


@api_view(['POST'])
def signup(request):
    data = request.data
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password
        serializer.save()
        return Response({"Sucess":"User created successfully"},status=201)
    else:
        return Response(serializer.errors,status=400)

@api_view(['GET'])
def travelplan(request):
    data = TravelPlan.objects.all()
    Data = []
    cnt = 0
    for i in data:
        booking = Booking.objects.filter(travel_id=i.travel_id)
        if booking:
            count = 0
            for j in booking:
                count+=j.member_count
            print(i.travel_id,count)
            Data.append(TravelPlanSerializer(i).data)
            Data[cnt].update({'total_count':count})
            cnt=cnt+1
    serializer = TravelPlanSerializer(data,many=True)
    return Response(Data)

@csrf_exempt
@api_view(['POST'])
def settravelplan(request):
    data = request.data
    serializer = TravelPlanSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Sucess":"Travel Plan created successfully"},status=201)
    else:
        return Response({"Failed":serializer.errors},status=400)

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
    except TravelPlan.DoesNotExist:
        return Response({"Failed":"No Travel Plan found"},status=400)
    
@csrf_exempt
@api_view(['DELETE'])
def deletetravelplan(request,travel_id):
    try:
        TPlan = TravelPlan.objects.get(travel_id=travel_id)
        image_file = TPlan.image
        if image_file:
            default_storage.delete(image_file.name)
        TPlan.delete()
        return Response("Travel Plan deleted successfully",status=200)
    except TravelPlan.DoesNotExist:
        return Response({"Failed":"No Travel Plan found"},status=400)


@api_view(['GET'])
def getbooking(request):
    data = Booking.objects.all()
    serializer = BookingSerializer(data,many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def getbookingof(request):
    try:
        session_id = request.data.get('sessionid')
        if session_id:
            session = Session.objects.get(session_key=session_id)
        email = session.get_decoded().get("email")
        user = User.objects.get(email=email)
        user_id = user.user_id
        bookings=Booking.objects.filter(user_id=user_id).order_by('booking_date')
        data = []
        count = 0
        for i in bookings:
            travel_id = BookingSerializer(i).data.get('travel')
            member_count = BookingSerializer(i).data.get('member_count')
            booking_price = BookingSerializer(i).data.get('booking_price')
            data.append(TravelPlanSerializer(TravelPlan.objects.get(travel_id=travel_id)).data)
            data[count].update({'member_count':member_count})
            data[count].update({'booking_price':booking_price})
            data[count].update({'booking_id':i.booking_id})
            count +=1
        return Response(data,status=200)
    except:
        return Response("invalid request",status=400)
    return Response("Invalid",status=400)

@csrf_exempt
@api_view(['POST'])
def booking(request):
    try:
        session_id = request.data.get('sessionid')
        if session_id:
            session = Session.objects.get(session_key=session_id)
        email = session.get_decoded().get("email")
        usr = User.objects.get(email=email)
        user = usr.user_id
        booking_price=request.data.get('booking_price')
        travel = request.data.get('travel')
        member_count = request.data.get('member_count')
        booking_date = request.data.get('booking_date')
        data = {"booking_price":booking_price,"travel":travel,"user":user,"member_count":member_count,"booking_date":booking_date}
        serializer = BookingSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Sucess":"Booked successfully"},status=201)
        else:
            return Response(serializer.errors,status=400)
    except:
        return Response({"Can't book this plan"},status=400)
    return Response("Invalid",status=400)

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
    except Booking.DoesNotExist:
        return Response({"Failed":"No Booking found"},status=400)

@csrf_exempt
@api_view(['DELETE'])
def deletebooking(request,booking_id):
    try:
        book = Booking.objects.get(booking_id=booking_id)
        book.delete()
        return Response("Booking deleted successfully",status=200)
    except Booking.DoesNotExist:
        return Response({"Failed":"Booking not found"},status=400)

@csrf_exempt
@api_view(['POST'])
def checkUser(request):
    session_id = request.data.get('sessionid')
    if not session_id:
        return Response({'message': 'Session ID not provided'}, status=400)
    try:
        session = Session.objects.get(session_key=session_id)
    except Session.DoesNotExist:
        return Response({'message': 'Invalid session ID'}, status=401)
    if session.expire_date < timezone.now():
        return Response({'message': 'Session has expired'}, status=401)

    session_data = session.get_decoded()
    email = session_data.get('email')

    if email:
        if User.objects.filter(email=email,role="ADMIN"):
            return Response("ADMIN",status=200)
        return Response("User",status=200)
    else:
        return Response({'message': 'Session is valid but not associated with a user'},status=400)