# Define the network client
from xrpl.clients import JsonRpcClient
def xrpl_connection():
    JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
    client = JsonRpcClient(JSON_RPC_URL)
    print(client, "XRP connected ")
    return client
