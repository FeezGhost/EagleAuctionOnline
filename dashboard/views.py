from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.models import User
import datetime
from django.contrib import messages
import re

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
        'now': now,
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

def bankedit(request):
    customer = request.user.customer
    useR = request.user
    userform = CreatUserForm(instance=customer)
    if request.method == 'POST':
        bank = request.POST.get("banks")
        ahc = request.POST.get("account_holder_name")
        an = request.POST.get("account_number")
        customer.banks = bank
        customer.account_holder_name = ahc
        customer.account_number = an
        customer.save()
        userform = CreatUserForm(instance=customer)

    context = {
        'CreatUserForm': userform,
    }
    return render(request, 'dashboard/dist/BankingEdit.html', context)

def coinstatus(request):
    customer = request.user.customer
    coins = customer.coins_set.all()
    bids = customer.bids_set.all()
    totalbids = bids.count()

    context = {
        'customer': customer,
        'coins':  coins,
        'bids': bids,
    }
    return render(request, 'dashboard/dist/CoinStatus.html', context)

def paybid(request):
    payer = request.user.customer
    payed = payer.buybid_set.all()
    context = {
        'payed': payed
    }
    return render(request, 'dashboard/dist/PayBids.html', context)

def receivepayments(request):
    bider = request.user.customer
    bids = bider.bids_set.all().order_by('-date_created')
    haveBuyer = []

    for bid in bids:
        haveBuyer.append(BuyBid.objects.filter(bider=bid))

    context = {
        'haveBuyer':haveBuyer,
        'bider':bider,
    }
    return render(request, 'dashboard/dist/ReceivePayments.html', context)

def declinepayment(request,pk_id):
    user = request.user.customer
    buybid =  BuyBid.objects.get(id=pk_id)
    bider = Bids.objects.get(id=buybid.bider.id)
    bider.remainingbid += buybid.quantity 
    if request.method == 'POST':
        buybid.status='declined'
        buy=buybid.save()
        bider1 = bider.save()
        return redirect("receive_payments")

    context = {
    }
    return render(request, 'dashboard/dist/DeclinePayment.html', context)

def acceptpayment(request,pk_id):
    user = request.user.customer
    buybid =  BuyBid.objects.get(id=pk_id)
    buyer = buybid.buyer
    coins = buyer.coins_set.all()
    quantity = buybid.quantity
    coinform = CoinsForm(instance=coins[0])
    totalup = coins[0].total
    remainingup = coins[0].remaining
    bidedup = coins[0].bided
    totalup +=int(quantity)
    remainingup +=int(quantity)
    if request.method == 'POST':
        buybid.status='approved'
        buy=buybid.save()
        coinform = CoinsForm({'customer':buyer, 'total':totalup,'bided': bidedup, 'remaining': remainingup} ,instance=coins[0])
        if coinform.is_valid():
            userCoinForm = coinform.save()
            return redirect("receive_payments")

    context = {
    }
    return render(request, 'dashboard/dist/AcceptPayment.html', context)

def paycustomer(request,pk_id):
    customer = request.user.customer
    bid = Bids.objects.get(id=pk_id)
    buyform = BuyBidForm(initial={'buyer':customer, 'bider':bid,'status':'pending'})
    bidformup = BidForm(instance=bid)


    bidcustomer = bid.customer
    bidauction = bid.auction
    bidbided = bid.bided
    remainingup = bid.remainingbid
    print(remainingup)

    value_bought = 0
    message1 = ''
    msg1 = False
    message2 = ''
    msg2 = False

    if request.method == 'POST':
        buyform = BuyBidForm(request.POST,  request.FILES)
        value_bought = int(request.POST.get("quantity"))

        remainingup = remainingup-value_bought

        if remainingup < 1:
            message1 = 'Remaining Coins are below than Bided Coins'
            msg1 = True
        
        else:
            message2 = 'Request for bid has been sent'
            msg2 = True
            bidformup = BidForm({'customer':bidcustomer, 'auction':bidauction, 'bided':bidbided, 'remainingbid': remainingup}, instance=bid)
            customerbuyform = BuyBidForm(request.POST,  request.FILES) 
            print(customerbuyform)
            

            if bidformup.is_valid():
                
                    bidformup2 = bidformup.save()
                    bidformup2.save()
                    print(bidformup2.id)
                    print(pk_id)
                    print("Bid form Updated")

            if buyform.is_valid():
                    print("buyform made")
                    buyform2 = buyform.save()

    context = {
        'bid':bid,
        'buyform':buyform,
        'message1': message1,
        'msg1': msg1,
        'message2': message2,
        'msg2': msg2,
    }

    return render(request, 'dashboard/dist/PayCustomer.html', context)

def auctiondetail(request):
    customer = request.user.customer
    latestauction  = ''
    coins = customer.coins_set.all()
    
    now = datetime.datetime.now().strftime('%H:%M:%S')
    hour = now.split(':')
    hours =   int(hour[0])
    mins = int(hour[1])


    live = False
    msg1 = msg2= False

    if((hours>10 and hours<11 )):
        live=True
        latestauction  = Auction.objects.last()
        allbids =latestauction.bids_set.all().order_by('-date_created')
    if (hours>18 and mins>30) and (hours<20 and mins<30):
        live=True

    allbids =''
    if live:
        latestauction  = Auction.objects.last()
        allbids =latestauction.bids_set.all().order_by('-date_created')

    bidform = BidForm(initial={'customer':customer, 'auction':latestauction})
    
    
    value_bided = 0
    mymessage = ""
    mymessage2 = ""


    coinform = CoinsForm(instance=coins[0])
    if request.method == 'POST':
        value_bided = int(request.POST.get("bided"))
        bidedup= coins[0].bided
        totalup = coins[0].total
        remainingup = coins[0].remaining
        if value_bided > remainingup:
            mymessage = "You don't have enough coins"
            msg1 = True
        else:
            value_bided = str(value_bided)
            bidedup +=int(value_bided)
            remainingup -=int(value_bided)
            remainingbid = int(value_bided)
            remainingup  = str(remainingup)
            bidedup = str(bidedup)
            coinform = CoinsForm({'customer':customer, 'total':totalup,'bided': bidedup, 'remaining': remainingup} ,instance=coins[0])
            if coinform.is_valid():
                userCoinForm = coinform.save()
                print(coinform)
                print(userCoinForm)
                
            bidform = BidForm(request.POST)
            print(bidform)
            print(request.POST.get("remainingbid"))
            if bidform.is_valid():
                bid =Bids.objects.create(
                    customer=customer, 
                    auction=latestauction, 
                    bided=value_bided, 
                    remainingbid= remainingbid
                )
                print(bid)
                mymessage2 = "Sucessfully  bided"
                msg2 = True

    context = {
        'customer': customer,
        'coins':  coins,
        'bidform':bidform,
        'coinform': coinform,
        'allbids': allbids,
        'mymessage': mymessage,
        'mymessage2': mymessage2,
        'live': live,
        'msg1': msg1,
        'msg2': msg2,
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
    
    now = datetime.datetime.now().strftime('%H:%M:%S')
    hour = now.split(':')
    hours =   int(hour[0])
    mins = int(hour[1])
    live = False
    if((hours>10 and hours<11)):
        live=True
    if (hours>18 and mins>30) and (hours<20 and mins<30):
        live=True
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR password is incorrect')
                
    context = {'live':live}
    return render(request,'dashboard/index.html',  context)
