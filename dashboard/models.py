from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    account_holder_name = models.CharField(max_length=200, null=True)
    account_number = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    CATEGORY = (
			('Capitec', 'Capitec'),
			('Absa', 'Absa'),
			('Nedbank', 'Nedbank'),
			('Standard Bank', 'Standard_bank'),
			('Tyme Bank', 'Tyme'),
			('Bidvest', 'Bidvest'),
			('African Bank', 'African_Bank'),
			('Gro bank south Africa', 'Gro_bank_south_Africa'),
			('FNB South Africa', 'FNB_South_Africa'),
			('FNB Namibia', 'FNB_Namibia'),
			('FNB South Africa', 'FNB_South_Africa'),
			('FNB Swaziland', 'FNB_Swaziland'),
			('FNB Zambia', 'FNB_Zambia'),
            ('FNB Lesotho', 'FNB_Lesotho'),
			)
    banks = models.CharField(max_length=200, null=True, choices=CATEGORY)
    
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

class ImmatureCoins(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    coins = models.IntegerField(default=0)
    days =models.IntegerField(default=0)
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
    remainingbid = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return str(self.date_created)

class BuyBid(models.Model):
    buyer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    bider = models.ForeignKey(Bids, null=True, on_delete= models.SET_NULL)
    quantity = models.IntegerField(default=0)
    CATEGORY = (
			('pending', 'Pending'),
			('approved', 'Approved'),
			('declined', 'Declined'),
			)
    status =models.CharField(max_length=200, null=True, choices=CATEGORY)
    
    CATEGORY1 = (
			('2', '2 Days'),
			('5', '5 Days'),
			)
    days =models.CharField(max_length=200, null=True, choices=CATEGORY1)
    proof = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return str(self.buyer.name)