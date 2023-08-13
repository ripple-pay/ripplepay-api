import xrpl
from apps.users.models import User
from apps.transactions.models import InitializePaymentModel, TransactionsModel
from .xrpl_connect import xrpl_connection
from xrpl.account import get_balance
from xrpl.models.transactions import Payment, OfferCreate
from xrpl.utils import xrp_to_drops
from xrpl.transaction import autofill_and_sign, submit_and_wait, submit
from asgiref.sync import sync_to_async
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.models.currencies import IssuedCurrency, XRP

xrp_client = xrpl_connection()

      
we_want = {
    "currency": IssuedCurrency(
        currency="USD",
        issuer="rg2MAgwqwmV9TgMexVBpRDK89vMyJkpbC"
    ),
    "value": "25",
}

we_spend = {
    "currency": XRP(),
    # 25 TST * 10 XRP per TST * 15% financial exchange (FX) cost
    "value": xrp_to_drops(25 * 10 * 1.15),
}
seed =  generate_faucet_wallet(xrp_client).seed
@sync_to_async
def create_offer(address):
    print("called", address)
    business_address = User.objects.get(classic_address = address)
    wallet = Wallet(business_address.public_key, business_address.private_key, seed=seed)
    tx = OfferCreate(
        account=wallet.address,
        taker_gets=we_spend["value"],
        taker_pays=we_want["currency"].to_amount(we_want["value"]),
    )
    # Sign and autofill the transaction (ready to submit)
    signed_tx = autofill_and_sign(tx, xrp_client, wallet) #Await keyword was removed
    print("Transaction:", signed_tx)

    # Submit the transaction and wait for response (validated or rejected)
    print("Sending OfferCreate transaction...")
    # result = submit_and_wait(signed_tx, xrp_client)
    result = submit(signed_tx, xrp_client)
    if result.is_successful():
        print(f"Transaction succeeded: "
                f"https://testnet.xrpl.org/transactions/{signed_tx.get_hash()}")
    else:
        raise Exception(f"Error sending transaction: {result}")