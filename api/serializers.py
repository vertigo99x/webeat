from rest_framework import serializers

from .models import Allusers, Vendor, Orders, Reviews, Events

from django.contrib.auth.models import User

class AllusersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allusers
        fields = "__all__"
        

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"
        
        
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"
        
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"
    
class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"
    
