from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('user/vendordata/<str:token>/', views.AlluserDataV.as_view()),
    path('user/clientdata/<str:username>/', views.AlluserDataC.as_view()),
    path('user/create/vendor/', views.RegisterVendor.as_view()),
    path('user/create/client/', views.RegisterClient.as_view()),
    path('vendors/food/<str:username>/', views.FoodDetails.as_view()),
    path('food/create/', views.CreateFoodDetails.as_view()),
]
