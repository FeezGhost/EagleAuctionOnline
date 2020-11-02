from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Coins)
admin.site.register(Bids)
admin.site.register(Auction)
admin.site.register(BuyBid)