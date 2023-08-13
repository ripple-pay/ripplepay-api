from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from utils.listener import WebsocketClass, main
from .serializers import (InitializePaymentSerializer, TransactionsModelSerializer)
from utils.xrpl_connect import xrpl_connection
from apps.users.models import User
from .models import InitializePaymentModel, WithdrawalModel
import os
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv
from django.http import HttpResponse
from utils.xrp_price import get_usd_eur, get_xrp_price
import math
import json
from .models import TransactionsModel
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.wallet import Wallet, generate_faucet_wallet
from xrpl.transaction import autofill_and_sign, submit_and_wait, submit
from datetime import datetime
from utils.add_trustline import create_trust_line
from django.views.decorators.csrf import csrf_exempt
load_dotenv()

xrp_client = xrpl_connection()
backend_domain = os.getenv("BACKEND_DOMAIN")
webSocketInstance = WebsocketClass()
seed =  generate_faucet_wallet(xrp_client).seed


class InitializePaymentViewSet(APIView):
    serializer_class = InitializePaymentSerializer
    @csrf_exempt
    def post(self, request):
        
        print(request.headers)
        api_key = request.headers['api-key']
        print(api_key)
        data = request.data
        currencies = ["EUR", "USD", "JPY", "NGN"]
        try:
            xrp_price = get_xrp_price() #Get xrp token price 
            if xrp_price['status']:
                business = User.objects.get(api_key=api_key)
                print(business.email, business.api_key)
                wallet = generate_faucet_wallet(xrp_client, debug=True)
                eur_jpy_response = get_usd_eur(data['amount'])
                for currency in currencies:
                    trustline = create_trust_line(private_key=wallet.private_key, public_key=wallet.public_key, seed=seed, issuer=os.getenv('ISSUER'), currency=currency, amount=1000000000) # Amount = 1*10*9
                transaction_ref = data['transaction_reference']
                xrp_amount = math.ceil((float(data['amount']) / float(xrp_price['price']))* 100)/100 # Get the xrp equivalence of amount to be paid, round to 2 d.p
                transaction_model = InitializePaymentModel.objects.create(
                    business= business,
                    wallet_address= wallet.classic_address,
                    wallet_public_key = wallet.public_key,
                    wallet_private_key = wallet.private_key,
                    amount= data['amount'],
                    transaction_reference = transaction_ref,
                    customers_email = data['customers_email'],
                    xrp_amount = xrp_amount,
                    eur = round(eur_jpy_response['EUR'], 2),
                    jpy = round(eur_jpy_response['JPY'],2),
                    ngn = round(eur_jpy_response['NGN'],2)
                    ) 
        
                serializer = self.serializer_class(transaction_model)
    
                serialized_data = serializer.data
                serialized_data['redirect_url'] = data['redirect_url']
                serialized_data['xrp_amount'] = xrp_amount
                serialized_data['business_name'] = business.business_name
                serialized_data['business_id'] = business.business_id
                serialized_data['payment_link'] = f"{backend_domain}/transactions/payment/tx-ref/{transaction_ref}"
                return Response(data={"message":"success", "data": serialized_data}, status=status.HTTP_200_OK)   
            return Response(data={"message": "failed"}, status=status.HTTP_400_BAD_REQUEST)       
        except Exception as e:
            return Response(data={"message": "failed"}, status=status.HTTP_400_BAD_REQUEST)
    
initialize_payment = InitializePaymentViewSet.as_view()

class TransactionsView(APIView):
    serializer_class = TransactionsModelSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = User.objects.get(email=request.user)
            transactions = TransactionsModel.objects.filter(business = user)
            serilaizer = self.serializer_class(transactions, many=True)
            return Response({"message":"success","data": serilaizer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        
        
    #The below function is for withdrawal to wallet
    def post(self, request):
        data = request.data
        res = {}
        payment =""
        business = User.objects.filter(email=request.user).first()
        if data['currency'] == "XRP":
            payment = Payment(account=business.classic_address, amount=xrp_to_drops(float(data['amount'])), destination=data['address'])  #Remove 10XRP Balance from amount to be transfered
        else:
            payment = Payment(account=business.classic_address,   amount= {
                        "currency":data['currency'],
                        "issuer":os.getenv('ISSUER'),
                        "value":data['amount']
                    }, destination=data['address'])  #Remove 10XRP Balance from amount to be transfered
        wallet = Wallet(business.public_key, business.private_key, seed=seed)
        #Sign transactions
        signed_tx = autofill_and_sign(payment, xrp_client, wallet)
        try:
            tx_response = submit(signed_tx, xrp_client)
            if tx_response.result["accepted"] == True:
                res['amount'] = data['amount']
                res['destination_adresss'] = data['address']
                res['source_address'] = business.classic_address
                res['date'] = datetime.today()
                WithdrawalModel.objects.create(business=business, address = data['address'], amount=data['amount'], currency=data['currency'])

                return Response({"message":"success","data":res }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, "Withdrawal error")
            return Response({"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        

transactions = TransactionsView.as_view()
            
        
def transactionsview(request, ref):
    initialize_payment_instance = InitializePaymentModel.objects.filter(transaction_reference=ref).first()
    context = {"address": initialize_payment_instance.wallet_address, 
               "customer": initialize_payment_instance.customers_email, 
               "usd": initialize_payment_instance.amount, "xrp": initialize_payment_instance.xrp_amount, 
               "business": initialize_payment_instance.business.business_name,
               "eur": initialize_payment_instance.eur,
               "jpy":initialize_payment_instance.jpy,
               "ngn": initialize_payment_instance.ngn
               }
    return render(request, 'transactions/transactions.html', context)


def custom_page_not_found(request, exception):
    return render(request, 'transactions/404.html', status=404)
