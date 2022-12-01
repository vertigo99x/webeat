from audioop import add
from django.shortcuts import render, Http404

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


from .models import Allusers, FoodItems, Reviews, Orders, Vendor, Events

from django.db.models import Q

from .serializers import VendorSerializer, AllusersSerializer, OrdersSerializer, ReviewsSerializer, EventsSerializer

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from django.conf import settings

from datetime import datetime

from threading import Thread

import time
import random

import json


def index(request):
    return render(request, "index.html")

class AlluserDataC(APIView):
    def get(self, request, username, format=None):
        userdata = Allusers.objects.filter(username=username)
        if len(userdata) == 0:
            return Response({'message':'user_doesnt_exist'})
        
        userdata = userdata[0]
        
        print(username.split('@')[-1])
        
        
        if userdata['usercat'].strip() == 'client':
            return Response(userdata)
       
        elif userdata['usercat'].strip() == 'vendor':
            vendordata = Vendor.objects.filter(username=username).values()[0]
            
            
            if int(vendordata['total_raters']) == 0:
                avg_rating = 'no_ratings_yet'
            else:
                avg_rating = int(vendordata['total_rating'])/int(vendordata['total_raters'])
            
            user_info = {
                'username':userdata['username'],
                'usercat':userdata['usercat'],
                'vendorname':vendordata['vendorname'],
                'image_link':userdata['image'],
                'business_email':vendordata['businessemail'],
                'business_phonenumber':vendordata['businessphonenumber'],
                'total_orders':vendordata['total_orders'],
                'business_address':vendordata['mainbusinessaddress'],
                'average_vendor_rating':f'{avg_rating}'
            }
            
            return Response(user_info)
        
        return ({'message':'invalid_category'})
            
class AlluserDataV(APIView):
    def get(self, request, token, format=None):
        
        is_token = Token.objects.filter(key=token).values()[0]
        user = User.objects.filter(id=is_token['user_id']).values()[0]['username']
        username = user
        
        userdata = Allusers.objects.filter(username=username).values()
        print(userdata)
        if len(userdata) == 0:
            return Response({'message':'user_doesnt_exist'})
        
        userdata = userdata[0]
        
        print(username.split('@')[-1])
        
        
        if userdata['usercat'].strip() == 'client':
            return Response(userdata)
       
        elif userdata['usercat'].strip() == 'vendor':
            vendordata = Vendor.objects.filter(username=username).values()[0]
            
            
            if int(vendordata['total_raters']) == 0:
                avg_rating = 'no_ratings_yet'
            else:
                avg_rating = int(vendordata['total_rating'])/int(vendordata['total_raters'])
            
            user_info = {
                'username':userdata['username'],
                'usercat':userdata['usercat'],
                'vendorname':vendordata['vendorname'],
                'image_link':userdata['image'],
                'business_email':vendordata['businessemail'],
                'business_phonenumber':vendordata['businessphonenumber'],
                'total_orders':vendordata['total_orders'],
                'business_address':vendordata['mainbusinessaddress'],
                'average_vendor_rating':f'{avg_rating}'
            }
            
            return Response(user_info)
        
        return ({'message':'invalid_category'})
            
            
class RegisterClient(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data['username'].strip()
        usercat='client'
        gender=data['gender'].strip()
        phonenumber=data['phonenumber'].strip()
        email = data['email'].strip()
        firstname=data['firstname'].strip()
        middlename=data['middlename'].strip()
        lastname=data['lastname'].strip()
        address=data['address'].strip()
        password=data['password']
        
        user = User.objects.filter(username=username).values()
        user_email = User.objects.filter(email=email).values()
        
        print(len(user),len(user_email))
        if len(user)==0 and len(user_email)==0:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save();

            user = Allusers.objects.create(
                username = username,
                usercat = usercat,
                firstname=firstname,
                gender=gender,
                middlename = middlename,
                lastname=lastname,
                address=address,
                phonenumber = phonenumber,
                email=email,
            )
            user.save();
            
            return Response({'message':'added_succesfully'})
        
        return Response({'message':'user_already_exists'})
    
    
class RegisterVendor(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data['username'].strip()
        usercat='vendor'
        vendor_name=data['vendor_name'].strip()
        gender=data['gender'].strip()
        phonenumber=data['business_phonenumber'].strip()
        email = data['business_email'].strip()
        firstname=data['firstname'].strip()
        middlename=data['middlename'].strip()
        lastname=data['lastname'].strip()
        address=data['address'].strip()
        password=data['password']
        
        user = User.objects.filter(username=username).values()
        vendordata = Vendor.objects.filter(vendorname=vendor_name).values()
        user_email = User.objects.filter(email=email).values()
        
        print(len(user),len(user_email),len(vendordata))
        if len(user)==0 and len(user_email)==0 and len(vendordata)==0:
            
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save();

            user = Allusers.objects.create(
                username = username,
                usercat = usercat,
                firstname=firstname,
                middlename = middlename,
                lastname=lastname,
                phonenumber = phonenumber,
                email=email,
            )
            user.save();
            
            vendor = Vendor.objects.create(
                username = username,
                vendorname = vendor_name,
                businessphonenumber = phonenumber,
                businessemail = email,
                mainbusinessaddress = address,               
                
            )
            event = Events.objects.create(
                sender='Eathub',
                recipient=username,
                message=f'Welcome to Eathub {vendor_name}',
                banner='primary'
            )
            event.save();
            
            return Response({'message':'added_succesfully','username':f'{username}'})
        
        return Response({'message':'user_already_exists'})



class Orders(APIView):
    def get(self, request, username, format=None):
        user = Allusers.objects.filter(username=username).values()[0]
        if user['usercat'] == 'client':
            client = Orders.objects.filter(client=username).all()
            serializer = OrdersSerializer(client, many=True)
            return Response(serializer)
        
        if user['usercat'] == 'vendor':
            vendor = Orders.objects.filter(vendor=username).all()
            serializer = OrdersSerializer(vendor, many=True)
            return Response(serializer)
        
    
    def post(self, request, *args, **kwargs):
        data = request.data
        
        food_id_array = data['cart_items'] # format = [{item_id:2,quan:2}]
        is_paid = data['is_paid_for']
        client = data['client_username']
        orderID = f'EATHUB{client[0:3].upper()}{random.randint(1000000,9999909)}'
        food_id_array_updated = {}
        total_price = 0
        for x in food_id_array:
            food = FoodItems.objects.filter(id=int(x['item_id'])).values()[0]
            vendor = food['vendor']
            price = int(food['price'])
            total_price += (price * int(x['quantity']))
            
            description = f"{food['title']} x {x['quantity']}"
            
            
            
        order = Orders.objects.create(
            client = client,
            vendor = vendor,
            food_items_array = json.dumps(food_id_array),
            order_description = description,
            order_id = orderID,
            total_price = total_price,
            is_payment_verified = True,
                
        )
        
        order.save();
        
        event = Events.objects.create(
            sender = vendor,
            recipient = client,
            message = "Your Order Has Been Sent",
            banner = 'primary',
        )
        event.save();
        
        return Response({'message':'submitted'})
            
            
    
class FoodDetails(APIView):
    def get(self, request, username, format=None):
        food = FoodItems.objects.filter(vendorusername=username).values()
        return Response(food)
        
class CreateFoodDetails(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        token = data['token']
        username = data['username']
        title = data['food_title']
        description = data['food_description']
        price = data['food_price']
        
        is_token = Token.objects.filter(key=token).values()[0]
        user = User.objects.filter(id=is_token['user_id']).values()[0]['username']
        userdata = Allusers.objects.filter(username=username).values()[0]
        usercat = userdata['usercat']
        
        if user == username and usercat == 'vendor':
            
            food = FoodItems.objects.create(
                vendorusername = username,
                food_title = title,
                food_description = description,
                food_price = price,
            )
            
            food.save();
            
            event = Events.objects.create(
                sender = 'Eathub',
                recipient = username,
                message = f"Item {title} has been added",
                banner = 'primary',
            )
            event.save();
                
            
            return Response({'message':'food_added_to_database'})
        
        return Response({'message':'user_not_valid'})
         
class Logout(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        token = data['token']
        Token.objects.filter(key=token).delete()
        
        return Response({'message':'loggged_out_successfully'})