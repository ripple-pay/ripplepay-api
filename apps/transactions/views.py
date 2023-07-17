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
from asgiref.sync import sync_to_async
from concurrent.futures import ThreadPoolExecutor
# from .consumers import main
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import concurrent.futures


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
            
            business = User.objects.get(api_key=api_key)
            wallet = generate_faucet_wallet(xrp_client, debug=True)
            transaction_ref = data['transaction_reference']
            xrp_amount = 1000
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
            serializer['payment_link'] = f"{backend_domain}/{transaction_ref}"
            return Response(data={"message":"success", "data": serializer.data}, status=status.HTTP_200_OK)          
        except Exception as e:
            return Response(data={"message": "failed"}, status=status.HTTP_400_BAD_REQUEST)
    
initialize_payment = InitializePaymentViewSet.as_view()



            

def transactionsview(request, ref):
   
 
    
  
    return render(request, 'transactions/transactions.html', {})