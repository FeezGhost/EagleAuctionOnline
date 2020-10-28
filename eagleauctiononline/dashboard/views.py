from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.models import User
import datetime
from django.contrib import messages

# from .forms import *

# Create your views here.
def dashboard(request):
    customer = request.user.customer
    coins = customer.coins_set.all()
    bids = customer.bids_set.all().order_by('-date_created')
    now = datetime.datetime.now().strftime('%H:%M:%S')
    context = {
        'customer': customer,
        'coins':  coins,
        'bids': bids,
        'now': now
    }
    return render(request, 'dashboard/dist/index.html', context)

def auctionhistory(request):
    customer = request.user.customer
    bids = customer.bids_set.all().order_by('-date_created')
    totalauctions = bids.count()

    context = {
        'customer': customer,
        'bids': bids,
        'totalauctions': totalauctions,
    }
    return render(request, 'dashboard/dist/AuctionHistory.html', context)

def bidmessages(request):
   return render(request, 'dashboard/dist/BIDMessages.html')

def coinstatus(request):
    customer = request.user.customer
    coins = customer.coins_set.all()
    # auctions = customer.auction_set.all().order_by('date_created')
    bids = customer.bids_set.all()
    totalbids = bids.count()
    # totalauctions = auctions.count()

    context = {
        'customer': customer,
        'coins':  coins,
        # 'auctions': auctions,
        'bids': bids,
    }
    return render(request, 'dashboard/dist/CoinStatus.html', context)

def paybid(request):
   return render(request, 'dashboard/dist/PayBids.html')

def receivepayments(request):
   return render(request, 'dashboard/dist/ReceivePayments.html')

def auctiondetail(request):
    customer = request.user.customer
    latestauction  = Auction.objects.last()
    coins = customer.coins_set.all()
    allbids =latestauction.bids_set.all().order_by('-date_created')
    now = datetime.datetime.now().strftime('%H:%M:%S')
    bidform = BidForm(initial={'customer':customer, 'auction':latestauction})
    value_bided = 0
    mymessage = ""
    mymessage2 = ""
    coinform = CoinsForm(instance=coins[0])
    hour = now.split(':')
    hours =   int(hour[0])
    print(hour[0])
    print(hours)
    if(hours>10):
        print('elligable')
    if request.method == 'POST':
        value_bided = int(request.POST.get("bided"))
        bidedup= coins[0].bided
        totalup = coins[0].total
        remainingup = coins[0].remaining
        if value_bided > remainingup:
            mymessage = "You don't have enough coins"
        else:
            value_bided = str(value_bided)
            bidedup +=int(value_bided)
            remainingup -=int(value_bided)
            remainingup  = str(remainingup)
            bidedup = str(bidedup)
            coinform = CoinsForm({'customer':customer, 'total':totalup,'bided': bidedup, 'remaining': remainingup} ,instance=coins[0])
            if coinform.is_valid():
                userCoinForm = coinform.save()
            bidform = BidForm(request.POST)
            if bidform.is_valid():
                userBidForm = bidform.save()
                mymessage2 = "Sucessfully  bided"
    print(value_bided)
    context = {
        'customer': customer,
        'coins':  coins,
        'bidform':bidform,
        'coinform': coinform,
        'allbids': allbids,
        'mymessage': mymessage,
        'mymessage2': mymessage2
    }
    return render(request, 'dashboard/dist/ViewAuction.html', context)


# @unauthenticated_user
def signupView(request):
    form = CreatUserForm()
    if request.method == 'POST':
        form = CreatUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user1 = form.cleaned_data.get('username')
            firstnname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')
            holdername = form.cleaned_data.get('account_holder_name')
            accountnumber = form.cleaned_data.get('account_number')
            phoneno = form.cleaned_data.get('phone')
            bank = form.cleaned_data.get('banks')
            customer=Customer.objects.create(
               user=user,
               name=user1,
               first_name=firstnname,
               last_name=lastname,
               account_holder_name=holdername,
               account_number=accountnumber,
               phone=phoneno,
               banks=bank,
            )

            Coins.objects.create(
               customer=customer,
            )
            messages.success(request, 'Account has been created for ' + user1)
            login(request, user)
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'dashboard/signup.html', context)

def logout_view(request):
    logout(request)
    return redirect("homepage")

def homepage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR password is incorrect')
                
    context = {}
    return render(request,'dashboard/index.html',  context)