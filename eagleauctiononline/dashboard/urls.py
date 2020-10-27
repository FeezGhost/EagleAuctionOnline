from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('Dashboard/', views.dashboard, name="dashboard"),
    path('AuctionHistory/', views.auctionhistory, name="auction_history"),
    path('BIDMessages/', views.bidmessages, name="bid_messages"),
    path('CoinStatus/', views.coinstatus, name="coin_status"),
    path('PayBids/', views.paybid, name="pay_bids"),
    path('ReceivePayments/', views.receivepayments, name="receive_payments"),
    path('ViewAuction/', views.auctiondetail, name="view_auction"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signupView, name="signup"),
]