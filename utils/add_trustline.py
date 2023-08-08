import xrpl
import json
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.requests.account_info import AccountInfo

testnet_url = "https://s.altnet.rippletest.net:51234"


def create_trust_line(private_key, public_key, seed, issuer, currency, amount):
    """create_trust_line"""
    receiving_wallet = Wallet(private_key=private_key,seed=seed, public_key=public_key)
    client = JsonRpcClient(testnet_url)
    trustline_tx=xrpl.models.transactions.TrustSet(
    account=receiving_wallet.classic_address,
    limit_amount=xrpl.models.amounts.IssuedCurrencyAmount(
        currency=currency,
        issuer=issuer,
        value=int(amount)
    )
)
    
    try:
        print("Creating trust line from hot address to issuer...")
        response = xrpl.transaction.submit_and_wait(trustline_tx, client, receiving_wallet)
        print(response)
        return response
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply = f"Submit failed: {e}"
        return reply