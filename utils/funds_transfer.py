from apps.users.models import User
from apps.transactions.models import InitializePaymentModel, TransactionsModel
from .xrpl_connect import xrpl_connection
from xrpl.account import get_balance
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.transaction import autofill_and_sign, submit_and_wait, XRPLReliableSubmissionException


#Transfer the sent in funds to the businness base address
#Create a transaction model for the business

xrp_client = xrpl_connection()

def funds_transfer(request, address):
    
    try:
        
        paymentInstance = InitializePaymentModel.objects.get(wallet_address = address)
        business = User.objects.get(pkid = paymentInstance.business.pkid)
        #Get balane of generated wallet
        balance = get_balance(address=paymentInstance.wallet_address, client=xrp_client, ledger_index="validated")
        #Prepare payment to base xrp account
        payment = Payment(account=paymentInstance.wallet_address, amount=xrp_to_drops(balance/1000000), destination=business.classic_address) 
        #Sign transactions
        signed_tx = autofill_and_sign(payment, xrp_client, paymentInstance.wallet_address)
        try:
            #Submit transaction to the xrp ledger
            tx_response = submit_and_wait(signed_tx, xrp_client)
            if tx_response["result"]["accepted"] == True:
                TransactionsModel.objects.create(wallet_address = paymentInstance.wallet_address, business = business, amount = paymentInstance.amount, transaction_reference = paymentInstance.transaction_reference, xrp_amount = paymentInstance.xrp_amount )
                
        except XRPLReliableSubmissionException as e:
            exit(f"Submit failed: {e}")
        
        
        pass
    except Exception as e:
        pass