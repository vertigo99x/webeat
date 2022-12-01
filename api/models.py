from django.db import models




class Allusers(models.Model):
    usercatChoices = [('vendor','vendor'),('client','client'),('dispatch','dispatch')]
    
    username = models.CharField(null=False, blank=False, max_length=255)
    usercat = models.CharField(null=False, blank=False, max_length=255, choices=usercatChoices)
    gender = models.CharField(null=False, blank=False, max_length=255)
    firstname = models.CharField(null=False, blank=False, max_length=255)
    middlename = models.CharField(null=True, blank=True, max_length=255)
    lastname = models.CharField(null=False, blank=False, max_length=255)
    phonenumber = models.CharField(null=False, blank=False, max_length=255)
    address = models.CharField(null=False, blank=False, max_length=255)
    email = models.CharField(null=True, blank=True, max_length=255)
    image = models.ImageField(upload_to=f'uploads/', blank=True, null=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username}"
    
    
    class Meta:
        ordering=['username']
        
        
class Vendor(models.Model):
    username = models.CharField(null=False, blank=False, max_length=255)
    vendorname = models.CharField(null=False, blank=False, max_length=255)
    businessphonenumber = models.CharField(null=False, blank=False, max_length=255)
    businessemail = models.CharField(null=True, blank=True, max_length=255)
    mainbusinessaddress = models.CharField(null=True, blank=True, max_length=255)
    total_rating = models.CharField(null=False, blank=False, max_length=255,default='0')
    total_raters = models.CharField(null=False, blank=False, max_length=255, default = '0')
    date_created = models.DateTimeField(auto_now_add=True)
    total_orders = models.IntegerField(null=False, blank=False, default = 0)
    total_revenue = models.IntegerField(null=False, blank=False, default = 0)
    wallet_balance = models.IntegerField(null=False, blank=False, default = 0)
    
    def __str__(self):
        return f"{self.vendorname}"
    
    
    class Meta:
        ordering=['vendorname']
        
        
class FoodItems(models.Model):
    vendorusername = models.CharField(null=False, blank=False, max_length=255)
    food_title = models.CharField(null=False, blank=False, max_length=255)
    food_description = models.CharField(null=False, blank=False, max_length=255)
    food_price = models.IntegerField(null=False, blank=False)
    total_rating = models.CharField(null=False, blank=False, max_length=255,default = '0')
    total_raters = models.CharField(null=False, blank=False, max_length=255, default = '0')
    image = models.ImageField(upload_to=f'uploads/food/', blank=True, null=True)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendorusername} -> {self.food_title}"
    
    class Meta:
        ordering=['food_title']
        
        
class Orders(models.Model):
    client = models.CharField(null=False, blank=False, max_length=255)
    vendor = models.CharField(null=False, blank=False, max_length=255)
    food_items_array = models.CharField(null=False, blank=False, max_length=255)
    order_description = models.CharField(null=False, blank=False, max_length=255)
    order_id = models.CharField(null=False, blank=False, max_length=255)
    total_price = models.IntegerField(null=False, blank=False)
    is_payment_verified = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.vendor} -> {self.order_id}"
    
    class Meta:
        ordering=['order_id']
    
class Reviews(models.Model):
    vendor = models.CharField(null=False, blank=False, max_length=255)
    client_username = models.CharField(null=False, blank=False, max_length=255)
    message = models.TextField(null=False, blank=False, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.client_username} <-> {self.vendor}"
    
    class Meta:
        ordering=['date_created']
    
class Events(models.Model):
    sender = models.CharField(null=False, blank=False, max_length=255)
    recipient = models.CharField(null=False, blank=False, max_length=255)
    message = models.CharField(null=False, blank=False, max_length=255)
    banner = models.CharField(null=False, blank=False, max_length=255)
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return f"{self.sender} <-> {self.recipient}"
    
    class Meta:
        ordering=['date_created']