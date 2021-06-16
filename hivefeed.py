import json
import threading, time, signal
import requests
from datetime import timedelta
from beem.transactionbuilder import TransactionBuilder
from beembase import operations
from beem import Hive

# API Definitions

api_coingecko = 'https://api.coingecko.com/api/v3/simple/price?ids=hive&vs_currencies=usd'

# Load Config and Connect blockchain instance

with open("config.json") as json_file:
    config = json.load(json_file)

# Wif below is for testing only, not a real wif
# Uncomment below and insert active wif and witness name if not using config.json

# wif= "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
#witness='sicarius'

# Comment out line below if not using .env
wif = config['keys']['active_key']
witness = config['witness'] #insert the name of your witness here



# Global function definitions

# Exception class for detecting program status
class ProgramKilled(Exception):
    pass

# Signal handler 
def signal_handler(signum, frame):
    raise ProgramKilled

# Helper function to obtain price from coingecko, can be expanded to add more apis
def get_price():
    res = requests.get(api_coingecko)
    #print(res.status_code)
    resData = res.text
    resJson = json.loads(resData)
    price = round(float(resJson['hive']['usd']), 3)
    #print(price)
    return price

# Instantiate blockchain instance
stm = Hive(keys=[wif])   

# Transaction building and broadcast function
def publish_price():
    #call api and get current aggregated price
    current_price = str(get_price()) + ' HBD'
    print("Attempting to publish current price: " + current_price)
    #Instantiate transaction object
    tx = TransactionBuilder(blockchain_instance=stm)
    #build operation object
    op = operations.Feed_publish(**{'publisher': witness,
                                    'exchange_rate': {'base':current_price, 'quote':'1.000 HIVE'}})
    #Append op to transaction
    tx.appendOps(op)
    #Append Wif to transaction
    tx.appendWif(wif)
    #Sign transaction
    tx.sign()
    #Broadcast transaction
    tx.broadcast()
    print("Successfully published price to feed!")


# Job class for instantiating thread with time delay ,clean execution and exit

class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        
    def stop(self):
                self.stopped.set()
                self.join()
    def run(self):
            while not self.stopped.wait(self.interval.total_seconds()):
                self.execute(*self.args, **self.kwargs)

# Time loop that instantiates Job classexecutes code            
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=config['publish_interval']), execute=publish_price)
    print("Starting Program..")
    job.start()
    
    while True:
          try:
              time.sleep(1)
          except ProgramKilled:
              print("Program killed: running cleanup code")
              job.stop()
              break

















