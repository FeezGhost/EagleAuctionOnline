from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.name)

class Coins(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    total = models.IntegerField(default=0)
    bided = models.IntegerField(default=0)
    remaining = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.customer.name



class Auction(models.Model):
    # time choices
    created_by = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.date_created)

class Bids(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    
    auction = models.ForeignKey(Auction, null=True, on_delete= models.SET_NULL)
    CATEGORY = (
			('500', 'R500'),
			('1000', 'R1000'),
			('2000', 'R2000'),
			('5000', 'R5000'),
			)
    bided =models.CharField(max_length=200, null=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return str(self.date_created)
