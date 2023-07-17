import asyncio
import websockets
import json
from apps.transactions.models import InitializePaymentModel
from concurrent.futures import ThreadPoolExecutor

# Using client libraries for ASYNC functions and websockets are needed in python.
# To install, use terminal command 'pip install asyncio && pip install websockets'


class WebsocketClass:
    
    # Handles incoming messages
    async def handler(self,websocket):
        message = await websocket.recv()
        return message

    # Use this to send API requests
    async def api_request(self,options, websocket):
        try:
            await websocket.send(json.dumps(options))
            message = await websocket.recv()
            return json.loads(message)
        except Exception as e:
            return e

    async def do_subscribe(self,websocket):
        print("calllllllllllllllllled")
        command = await self.api_request({
            'command': 'subscribe',
            'accounts': ['rwDJ3sxq3eMZRrGgDKGQcV26JyfhAuky8b']
            }, websocket)

        if command['status'] == 'success':
            print('Successfully Subscribed!')
        else:
            print("Error subscribing: ", command)
        data = await self.handler(websocket)
        datum = json.loads(data)
        if(datum['transaction']['Destination']== "rwDJ3sxq3eMZRrGgDKGQcV26JyfhAuky8b" & datum['transaction']['TransactionType'] == "Payment"):
            print(datum['transaction'])
        else:
            pass


    async def run(self):
        # Opens connection to ripple testnet
        async for websocket in websockets.connect('wss://s.altnet.rippletest.net:51233'):
            try:

                await self.do_subscribe(websocket)
            except websockets.ConnectionClosed:
                print('Disconnected...')


webSocketInstance = WebsocketClass()

def main():
    print("called")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(webSocketInstance.run())
    print("Passed")
    loop.close()
    print('Restarting Loop')

if __name__ == '__main__':
    main()
    
    


