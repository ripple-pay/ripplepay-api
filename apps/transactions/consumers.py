import asyncio
import websockets
import json
from channels.generic.websocket import AsyncWebsocketConsumer
# Using client libraries for ASYNC functions and websockets are needed in python.
# To install, use terminal command 'pip install asyncio && pip install websockets'

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

# Tests functionality of API_Requst
async def pingpong(websocket):
    command = {
        "id": "on_open_ping_1",
        "command": "ping"
    }
    value = await api_request(command, websocket)
    print(value)

async def do_subscribe(websocket):
    command = await api_request({
        'command': 'subscribe',
        'accounts': ['rwDJ3sxq3eMZRrGgDKGQcV26JyfhAuky8b']
        }, websocket)
    if command['status'] == 'success':
            print('Successfully Subscribed!')
    else:
        pass
    data = await handler(websocket)
    datum = json.loads(data)
    if(datum['transaction']['Destination']== "rwDJ3sxq3eMZRrGgDKGQcV26JyfhAuky8b" and datum['transaction']['TransactionType'] == "Payment"):
        print(datum['transaction'])
    else:
        pass

      
    

async def run():
    # Opens connection to ripple testnet
    async for websocket in websockets.connect('wss://s.altnet.rippletest.net:51233'):
        try:
           await pingpong(websocket)
           await do_subscribe(websocket)
        except websockets.ConnectionClosed:
            print('Disconnected...')


class ExternalWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None):
        print("data", text_data)
        await run()