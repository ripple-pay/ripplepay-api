# RipplePay-Description
  * Ripplepay is a mutli-currency cross-border business to business  payment solution that is built on the xrp ledger.
  * This API is written using python, django and django rest framework.
# Third Party API Services
  # Messari 
    * Messari was used in this project to get the current price of 1XRP token to 1USD
    * Create a .env file at the root of your project and add MESSARI_XRP_ASSET_URL=https://data.messari.io/api/v1/assets/xrp/metrics
  # CurrencyFreak 
    * Signup on currency freak and get copy your api-key. Currency freak provided us with the forex exchange value of 1USD to 1EUR, 1USD to JPY and 1USD to 1NGN
    * Add CURRENCY_FREAK_API_KEY="api-key" your .env file.
  # Trustline Issuer
   * The Issuer us provided with the ability to add a few currency [EUR, JPY, NGN, USD] trustlines to customers xrp wallet addresses.
   * Add ISSUER=rg2MAgwqwmV9TgMexVBpRDK89vMyJkpbC to your .env file
   * Add your backend url to the .env file as BACKEND_DOMAIN=http://localhost:8000
   * Dont forget to add your project signing key to the .env file as SIGNING_KEY=""

# Things to note when testing locally
* Must have an internet connection
* Start your django server
* Start your redis server using "redis-server" as cmd.
  
# How to generate payment link for customers on testnet
* Endpoint: http://localhost:8000/transactions/initialize-payment
* Request body: {"amount":10, "transaction_reference":"abcde", "customers_email":"customer@gmail.com", 
   "redirect_url":"wwww.google.com"}
* Add your business api-key to the request header as a key pair-value. {"api-key": "value"}
* Your request method should be a post request.
  
