import json
import requests
from beem.transactionbuilder import TransactionBuilder
from beembase import operations
from beem import Hive

# API Definitions

api_coingecko = 'https://api.coingecko.com/api/v3/simple/price?ids=hive&vs_currencies=usd'

# Load Config and Connect blockchain instance

with open("config.json") as json_file:
    config = json.load(json_file)

#print(config)

# Wif is for testing only, not a real wif
wif="5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3" #place private wif signing key here
witness="sicarius" #insert the name of your witness here

stm = Hive(nobroadcast=True)

# Global function definitions

# Function to obtain price from coingecko, can be expanded to add more apis
def get_price():
    res = requests.get(api_coingecko)
    #print(res.status_code)
    resData = res.text
    resJson = json.loads(resData)
    price = round(float(resJson['hive']['usd']), 3)
    #print(price)
    return price

# Transaction building and execution
current_price = str(get_price()) + ' HIVE'

tx = TransactionBuilder(blockchain_instance=stm)

op = operations.Feed_publish(**{'publisher': witness,
                                'exchange_rate': {'base':current_price, 'quote':'1.000 HBD'}})

tx.appendOps(op)
tx.appendWif(wif)
tx.sign()
print(tx.broadcast())















