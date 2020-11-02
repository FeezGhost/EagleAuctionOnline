from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreatUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='First Name.', label='First Name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Optional.' ,label='Last Name')
    account_holder_name = forms.CharField(max_length=30, required=True)
    account_number = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=30 , required=True)
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
			)
    banks = forms.ChoiceField(choices=CATEGORY)

		
    class Meta:
        model =  User
        fields =  ['username', 'first_name', 'last_name', 'email', 'phone', 'account_holder_name','account_number', 'banks','password1', 'password2']

class BidForm(ModelForm):
    
    class Meta:
        model = Bids
        fields = '__all__'
    

class CoinsForm(ModelForm):
    
    class Meta:
        model = Coins
        fields = '__all__'

class BuyBidForm(ModelForm):
    
    class Meta:
        model = BuyBid
        fields = '__all__'