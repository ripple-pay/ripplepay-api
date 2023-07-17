from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from .serializers import (RegisterBusinessSerializer)
from utils.utils import generate_business_id
from utils.xrpl_connect import xrpl_connection
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.requests.account_info import AccountInfo
from xrpl.account import get_balance
from .models import User

xrp_client = xrpl_connection()





class RegisterBusiness(APIView):
    serializer_class = RegisterBusinessSerializer

    def post(self,request):
        data = request.data
        business_id = generate_business_id()
        try:
            #Make all fields required in the frontend 
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                wallet = generate_faucet_wallet(xrp_client, debug=True)
                user = serializer.save()  
                user.set_password(data['password'])
                user.business_id = business_id
                user.classic_address = wallet.classic_address
                user.private_key = wallet.private_key
                user.public_key = wallet.public_key
                user.save()   
                # serialized_data = self.serializer_class(saved_user)
                
                return Response(data=serializer.data, status= status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status= status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            print(e,"+++++++++++++++")
            # logging.info(f"Error occured during signup : {e}")
            return Response(data={"message": "Error occured during signup"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        try:
            user = User.objects.get(email=request.user)
            balance = get_balance(address=user.classic_address, client=xrp_client, ledger_index="validated")
            serializer = self.serializer_class(user)
            serializer['balance'] = balance
            return Response(data={"message":"success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"message":"failed", "data": "Failed process"}, status=status.HTTP_400_BAD_REQUEST)
        
          
        
business = RegisterBusiness.as_view()