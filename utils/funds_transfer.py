import os
import xrpl
from apps.users.models import User
from apps.transactions.models import InitializePaymentModel, TransactionsModel
from .xrpl_connect import xrpl_connection
from xrpl.account import get_balance
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.transaction import autofill_and_sign, submit_and_wait, submit
from asgiref.sync import sync_to_async
from xrpl.wallet import generate_faucet_wallet, Wallet
from .convert_to_sable_coin import create_offer


#Transfer the sent in funds to the businness base address
#Create a transaction model for the business

xrp_client = xrpl_connection()
seed =  generate_faucet_wallet(xrp_client).seed

@sync_to_async
def funds_transfer(address, transaction_details):
    try:  
        paymentInstance = InitializePaymentModel.objects.filter(wallet_address = address).first() #Get the instance of the generated wallet address
        business = User.objects.get(pkid = paymentInstance.business.pkid) #Get the business of that the wallet was generated for
        # balance = get_balance(address=paymentInstance.wallet_address, client=xrp_client, ledger_index="validated") #Get the balance of the generated wallet address
        #Transfer of native  xrp token
        wallet = Wallet(paymentInstance.wallet_public_key, paymentInstance.wallet_private_key, seed=seed)
        if type(transaction_details) == str:
            print("Sending native xrp")
            payment = Payment(account=paymentInstance.wallet_address, amount=xrp_to_drops(float(paymentInstance.xrp_amount)), destination=business.classic_address)  #Remove 10XRP Balance from amount to be transfered
            #Sign transactions
            signed_tx = autofill_and_sign(payment, xrp_client, wallet)
            try:

                tx_response = submit(signed_tx, xrp_client)
                if tx_response.result["accepted"] == True:
                    print(tx_response, "transactions response")
                    TransactionsModel.objects.create(wallet_address = paymentInstance.wallet_address, business = business, amount = paymentInstance.amount, transaction_reference = paymentInstance.transaction_reference, xrp_amount = paymentInstance.xrp_amount, customers_email = paymentInstance.customers_email, currency = "XRP" )
                    #Send webhook data to business url that received the payment
                    #Webhook section
                    # create_offer("raE4x4cX2BYUcDJ3tSD2XGBfm2iwiBLP6y")
                 
                        
                    
            except (Exception) as e:
                # print(e, "Error")
                exit(f"Submit failed: {e}")
        else:
 
            try:
                send_token_tx = Payment(
                    account=paymentInstance.wallet_address,
                    destination=business.classic_address,
                    amount= {
                        "currency":transaction_details['currency'],
                        "issuer":os.getenv('ISSUER'),
                        "value":transaction_details['value']
                    }
                )

                # print(f"Sending {issue_quantity} {currency_code} to {hot_wallet.address}...")
                print("Sending issued currency")
                signed_tx = autofill_and_sign(send_token_tx, xrp_client, wallet)
                print("SIGNED TX:::::::::::::::::::::::::::::::")
                tx_response = submit(signed_tx, xrp_client)
             
                if tx_response.result["accepted"] == True:
                    print("SENT ISSUED CURRENCY")
                    TransactionsModel.objects.create(wallet_address = paymentInstance.wallet_address, business = business, amount = paymentInstance.amount, transaction_reference = paymentInstance.transaction_reference, xrp_amount = transaction_details['value'], customers_email = paymentInstance.customers_email, currency = transaction_details['currency'] )
            except Exception as e:
                pass
        
    except Exception as e:
        # print(e, "Funds transfer Error")
        pass
    



