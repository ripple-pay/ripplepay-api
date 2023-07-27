import asyncio
import websockets
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import TransactionsModel, InitializePaymentModel
from apps.users.models import User
from utils.funds_transfer import funds_transfer
from utils.convert_to_sable_coin import create_offer
import json
from asgiref.sync import sync_to_async
from xrpl.wallet import Wallet

from xrpl.models.requests.account_info import AccountInfo
from utils.xrpl_connect import xrpl_connection
from xrpl.account import get_balance
from .models import User
from datetime import date
from dateutil.relativedelta import relativedelta
from xrpl.wallet import Wallet


# Using client libraries for ASYNC functions and websockets are needed in python.
# To install, use terminal command 'pip install asyncio && pip install websockets'

xrp_client = xrpl_connection()

# Handles incoming messages
async def handler(websocket):
    message = await websocket.recv()
    return message

# Use this to send API requests
async def api_request(options, websocket):
    try:
        await websocket.send(json.dumps(options))
        message = await websocket.recv()
        print(message, "message")
        return json.loads(message)
    except Exception as e:
        return e

async def do_subscribe(wallet_address, websocket):
    print(wallet_address, "This is wallet")
    command = await api_request({
        'command': 'subscribe',
        'accounts': [str(wallet_address)]
        }, websocket)
    if command['status'] == 'success':
            print('Successfully Subscribed!')
    else:
        pass
    data = await handler(websocket)
    datum = json.loads(data)
    #Check if the address that received the payment is the address we subscribed to
    if(datum['transaction']['Destination']== str(wallet_address) and datum['transaction']['TransactionType'] == "Payment"):
        print("hii")
        funds_transfer_instance = await funds_transfer(wallet_address) #Transfer the funds from generated adddress to base address
    else:
        pass

      

async def run(wallet_address):
    # Opens connection to ripple testnet
    async for websocket in websockets.connect('wss://s.altnet.rippletest.net:51233'):
        try:
        #    await pingpong(websocket)
           await do_subscribe(wallet_address,websocket)
        except websockets.ConnectionClosed:
            print('Disconnected...')
            
@sync_to_async
def getPaymentInstance(text_data):
    #Get the transaction reference from the frontend websocket connection
    #Get the paymentInstanceModel of the transactionReference
    payment_instance = InitializePaymentModel.objects.filter(transaction_reference = text_data).first()
    return payment_instance.wallet_address


class ExternalWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    async def receive(self, text_data=None, bytes_data=None):
        payment_instance_wallet = await getPaymentInstance(text_data)
    
        print(payment_instance_wallet, "Wallet address")
        await run(payment_instance_wallet) #Pass the wallet of the payment Instance to the run function()
       
    