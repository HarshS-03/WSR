from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name    
    
class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=125)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    price = models.IntegerField()
    srtdesc = models.CharField(max_length=225,verbose_name="Short Description")
    qty=models.IntegerField(default=50,verbose_name="Quantity")
    desc =models.TextField(verbose_name="Description")
    profit=models.IntegerField(default=0,verbose_name="Profit on Product(%)")
    timestamp= models.DateTimeField(default=now)
    
    def __str__(self):
        return self.name    
    
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    sub = models.CharField(max_length=100)
    desc = models.TextField(max_length=300,default="")
    
    def __str__(self):
        return self.sub + " by " + self.email
    
class customerOrder(models.Model):
    CHOICES1 = (
        ("Processing",'Processing'),
        ("Done",'Done'),
    )    
    CHOICES2 = (
        ("COD",'Cash on Delivery'),
        ("Done",'Done'),
    )
    orderId = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    productdetails = models.TextField(verbose_name="Product Details")
    totalprice = models.IntegerField(verbose_name="Total Price")
    firstname = models.CharField(max_length=100,verbose_name="First name")
    lastname = models.CharField(max_length=100,verbose_name="Last name")
    address = models.TextField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    pincode = models.IntegerField()
    phone = models.CharField(max_length=15)
    timestamp= models.DateTimeField(default=now)
    status = models.CharField(max_length=20,choices=CHOICES1,default="Processing")        
    payment = models.CharField(max_length=20,choices=CHOICES2,default="COD")        
    
    def __str__(self):
        return  str(self.orderId) +"  |  " + self.email 

class updateStatus(models.Model):
    orderId=models.ForeignKey(customerOrder,on_delete=models.CASCADE,default='',null=True)
    status=models.CharField(max_length=300,default='',null=True)
    
    def __str__(self):
        return  str(self.orderId) 
    
class userreview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,default='')
    message=models.TextField(default='')
    verbose_name = "User Review"
    
    def __str__(self):
        return  self.user.username
    
class cacnceledorder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    reason=models.TextField(default='')
    
    def __str__(self):
        return  self.user.username
    
