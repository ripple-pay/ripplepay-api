from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from utils.listener import WebsocketClass, main
from .serializers import InitializePaymentSerializer
from utils.xrpl_connect import xrpl_connection
from xrpl.wallet import generate_faucet_wallet
from apps.users.models import User
from .models import InitializePaymentModel
import os
import asyncio
from dotenv import load_dotenv
from django.http import HttpResponse
from utils.xrp_price import get_xrp_price
import math


load_dotenv()

xrp_client = xrpl_connection()
backend_domain = os.getenv("BACKEND_DOMAIN")
webSocketInstance = WebsocketClass()


#Code funcs
#Create a wallet for an order
#Subscribe to listen to incoming payments
#Generate a new payment link for the order created

class InitializePaymentViewSet(APIView):
    serializer_class = InitializePaymentSerializer
    def post(self, request):
        api_key = request.headers['api_key']
        data = request.data
        try:
            xrp_price = get_xrp_price() #Get xrp token price 
            if xrp_price['status']:
                business = User.objects.get(api_key=api_key)
                wallet = generate_faucet_wallet(xrp_client, debug=True)
                
                transaction_ref = data['transaction_reference']
                xrp_amount = math.ceil((float(data['amount']) / float(xrp_price['price']))* 100)/100 # Get the xrp equivalence of amount to be paid, round to 2 d.p
                transaction_model = InitializePaymentModel.objects.create(
                    business= business,
                    wallet_address= wallet['classic_address'],
                    wallet_public_key = wallet['public_key'],
                    wallet_private_key = wallet['private_key'],
                    amount= data['amount'],
                    transaction_reference = transaction_ref,
                    xrp_amount = xrp_amount
                    ) 
                serializer = self.serializer_class(transaction_model)
                serializer['redirect_url'] = data['redirect_url']
                serializer['xrp_amount'] = xrp_amount
                serializer['business_name'] = business.business_name
                serializer['business_id'] = business.business_id
                serializer['payment_link'] = f"{backend_domain}/transactions/tx-ref={transaction_ref}"
                return Response(data={"message":"success", "data": serializer.data}, status=status.HTTP_200_OK)   
            return Response(data={"message": "failed"}, status=status.HTTP_400_BAD_REQUEST)       
        except Exception as e:
            return Response(data={"message": "failed"}, status=status.HTTP_400_BAD_REQUEST)
    
initialize_payment = InitializePaymentViewSet.as_view()



            

def transactionsview(request, ref):
    return render(request, 'transactions/transactions.html', {})
# 

def custom_page_not_found(request, exception):
    return render(request, 'transactions/404.html', status=404)
