# RipplePay-Description
  * Ripplepay is a mutli-currency business to business solution that is built on xrp ledger.
  * The API is written in python programming language.
# Third Party API Services
  # Messari 
    * Messari was used in this project to get the current price of 1XRP token to 1USD
    * Create a .env file at the root of your project and add MESSARI_XRP_ASSET_URL=https://data.messari.io/api/v1/assets/xrp/metrics
  # CurrencyFreak 
    * Signup on currency freak and get copy your api-key. Currency freak provided us with the forex exchange value of 1USD to 1EUR, 1USD to JPY and 1USD to 1NGN
    * Add CURRENCY_FREAK_API_KEY="api-key" your .env file.
  # Trustline Issuer
   * The Issuer was provided with the ability to add a few currency [EUR, JPY, NGN, USD] trustlines to customers xrp wallet addresses.
   * Add ISSUER=rg2MAgwqwmV9TgMexVBpRDK89vMyJkpbC to your .env file


  
