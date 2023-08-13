from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from .serializers import (LoginSerializer, RegisterBusinessSerializer)
from utils.id_generators import businessIDGenerator, apiKeyGenerator
from utils.xrpl_connect import xrpl_connection
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.requests.account_info import AccountInfo
from xrpl.account import get_balance
from .models import User
from datetime import date
from dateutil.relativedelta import relativedelta
from xrpl.wallet import Wallet
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from apps.transactions.models import TransactionsModel
from utils.add_trustline import create_trust_line
from dotenv import load_dotenv
from xrpl.models.requests import AccountLines
import os
load_dotenv()


xrp_client = xrpl_connection()
three_months = date.today() + relativedelta(months=+3)
seed =  generate_faucet_wallet(xrp_client).seed

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self,request):
        try:
            data = request.data
            email = data['email']
            password = data['password']
            user = User.objects.get(email= email)
        
            refresh = RefreshToken.for_user(user)
            raw_token = str(refresh.access_token)   
         
            if user is None:
                raise AuthenticationFailed(detail="User Not Found ")
            if not user.check_password(password):
                raise AuthenticationFailed(detail="Password is Incorrect")
            serializer = self.serializer_class(user, context= {'request': request})
            return Response(data ={"data":serializer.data,"refresh": str(refresh), "access": raw_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"message": "Failure occurred during log in"}, status=status.HTTP_400_BAD_REQUEST)
        

login_view = LoginView.as_view()


class RegisterBusiness(APIView):
    serializer_class = RegisterBusinessSerializer

    def post(self,request):
        data = request.data
        business_id = businessIDGenerator()
        api_key = apiKeyGenerator()
        currencies = ["EUR", "USD", "JPY", "NGN"]
        try:
            #Make all fields required in the frontend 
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                wallet = generate_faucet_wallet(xrp_client, debug=True)
                #add trustlines to created wallets 
                for currency in currencies:
                    trustline_reply = create_trust_line(private_key=wallet.private_key,public_key=wallet.public_key, seed=seed,issuer=os.getenv('ISSUER'),currency= currency,amount= 1000000000) # amount is  1 *10**9
              
                user = serializer.save()  
                user.set_password(data['password'])
                user.business_id = business_id
                user.classic_address = wallet.classic_address
                user.private_key = wallet.private_key
                user.public_key = wallet.public_key
                user.api_key = api_key
                user.api_key_expiration = three_months
                user.account_activated = True
                user.save()   
                
                return Response(data=serializer.data, status= status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status= status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response(data={"message": "Error occured during signup"}, status=status.HTTP_400_BAD_REQUEST)
          
        
business = RegisterBusiness.as_view()

class GetBalanceAndCustomersCountAPIView(APIView):
    #Get account and all the trustlines balances associated with the base address
        permission_classes = [IsAuthenticated]
        def get(self,request):
            data ={}
            try:
                user = User.objects.get(email=request.user)
                balance = get_balance(address=user.classic_address, client=xrp_client, ledger_index="validated")
                account_lines_request = AccountLines(account=user.classic_address)
                response = xrp_client.request(account_lines_request)
                trustlines = response.result["lines"]
                for trustline in trustlines:
                    if trustline['currency'] == "JPY":
                        data['jpy'] =  trustline['balance']
                    if trustline['currency'] == "EUR":
                        data['eur'] =  trustline['balance']
                    if trustline['currency'] == "USD":
                        data['usd'] =  trustline['balance']
                    if trustline['currency'] == "NGN":
                        data['ngn'] =  trustline['balance']
                    
                # customers = TransactionsModel.objects.distinct('customers_email').count() // Worrks for postgresql db not mysql
                
                data['balance'] = balance
                return Response(data={"message":"success", "data": data}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={"message":"failed", "data": "Failed process"}, status=status.HTTP_400_BAD_REQUEST)

balance_customer_count = GetBalanceAndCustomersCountAPIView.as_view()


class ActivateAccount(APIView):
    "Activating account, allows the user to add trustlines like EUR, USD, JPY and NGN"
    permission_classes =[IsAuthenticated]
    def patch(self, request):
        currencies = ["EUR", "USD", "JPY", "NGN"]
        account = User.objects.get(email=request.user)
        try:
            for currency in currencies:
                trustline_reply = create_trust_line(private_key=account.private_key,public_key=account.public_key, seed=seed,issuer=os.getenv('ISSUER'),currency= currency,amount= 1000000000) # amount is  1 *10**9
            account.account_activated = True
            account.save()
            return Response({}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": {e}}, status=status.HTTP_400_BAD_REQUEST)

activate_account = ActivateAccount.as_view()
        
        
        
    
            

