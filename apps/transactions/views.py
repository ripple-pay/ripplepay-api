from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from utils.listener import WebsocketClass, main
from .serializers import (InitializePaymentSerializer, TransactionsModelSerializer)
from utils.xrpl_connect import xrpl_connection
from xrpl.wallet import generate_faucet_wallet
from apps.users.models import User
from .models import InitializePaymentModel
import os
from rest_framework.permissions import IsAuthenticated
import asyncio
from dotenv import load_dotenv
from django.http import HttpResponse
from utils.xrp_price import get_xrp_price
import math
import json
from .models import TransactionsModel


load_dotenv()

xrp_client = xrpl_connection()
backend_domain = os.getenv("BACKEND_DOMAIN")
webSocketInstance = WebsocketClass()


class InitializePaymentViewSet(APIView):
    serializer_class = InitializePaymentSerializer
    def post(self, request):
        print(request.headers)
        api_key = request.headers['api_key']
        data = request.data
        try:
            xrp_price = get_xrp_price() #Get xrp token price 
            if xrp_price['status']:
                business = User.objects.get(api_key=api_key)
                wallet = generate_faucet_wallet(xrp_client, debug=True)
                print(wallet)
                
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
                    xrp_amount = xrp_amount
                    ) 
        
                serializer = self.serializer_class(transaction_model)
    
                serialized_data = serializer.data
                serialized_data['redirect_url'] = data['redirect_url']
                serialized_data['xrp_amount'] = xrp_amount
                serialized_data['business_name'] = business.business_name
                serialized_data['business_id'] = business.business_id
                serialized_data['payment_link'] = f"{backend_domain}/transactions/tx-ref/{transaction_ref}"
                return Response(data={"message":"success", "data": serialized_data}, status=status.HTTP_200_OK)   
            return Response(data={"message": "failed"}, status=status.HTTP_400_BAD_REQUEST)       
        except Exception as e:
            print(e)
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
        

transactions = TransactionsView.as_view()
            
    
                

def transactionsview(request, ref):
    return render(request, 'transactions/transactions.html', {})
# 

def custom_page_not_found(request, exception):
    return render(request, 'transactions/404.html', status=404)
