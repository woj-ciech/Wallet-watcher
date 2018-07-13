import requests
import json
import datetime
import sys
import argparse
from termcolor import colored

parser = argparse.ArgumentParser(
    description='Wallet watcher',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter #added to show default value


)
print colored("asciiart.eu    ______________ \n\
  __,.,---'''''              '''''---..._\n\
,-'             .....:::''::.:            '`-.\n\
'           ...:::.....       '''\n\
|           ''':::'''''       .              |\n\
|'-.._           ''''':::..::':          __,,-\n\
'-.._''`---.....wallet watcher.....---''__,,-\n\
    ''`---.....________________.....---''", "yellow")
print "github.com/woj-ciech medium.com/@woj_ciech\n"
print "Example: wallet-watcher.py --address \"1Bd8evxVYZLF6FVNQpUGuwvzgqvoMVK2Lx, 1Jc65vRz6qC3r9XmGpmoEGBKmDZXc9sfNv\" --begin 7 --end 19 --json\n"

parser.add_argument("--address", help="Address(es) in format: \"xxx, yyy\"",
                    default="1Nhztc2zhxzqqhTYFUE6bJw9sJAwTu7yYF")
parser.add_argument("--begin", help="Hour from which to start",
                    default="9",type=int)
parser.add_argument("--end", help="Hour from which to end",
                    default="17", type=int)
parser.add_argument('--json', help='JSON output. wallet_name.txt in current directory',
                    action='store_true')

args = parser.parse_args()

btc_address = args.address
beginning = args.begin
end = args.end
json_output = args.json

#check for given timestamp
def check_hours(start, end):
    if start > end:
        print("ERROR")
        sys.exit()

#dump to json
def to_json(filename, input):
    with open(filename + '.json', 'w') as outfile:
        json.dump(input, outfile, indent=4, sort_keys=True, default=str)

#check request
def check_request(request):
    if request.status_code != 200:
        print "Connection error or wrong address"
        sys.exit()


check_hours(beginning,end)

address = {"addr": btc_address}

print "Checking all transactions of %s from %s to %s" % (colored(btc_address,'green'), colored(beginning, 'red'), colored(end,'red'))
print "JSON output: " + str(json_output)

history = requests.post("https://www.blockonomics.co/api/searchhistory", json=address) #request co blockonomics.co, json=addresses seperated by whitespaces
check_request(history)

transactions = json.loads(history.content) #load json
data_output = {}

for i in transactions['history']:
    satoshis = i['value'] #get value of payment (if value is negative it means that payment was outgoing, otherwise incoming)
    timestamp = datetime.datetime.fromtimestamp(
                int(i['time'])) #get timestamp of transaction
    timestamp_string = timestamp.strftime('%Y-%m-%d %H:%M:%S')


    if satoshis > 0 and beginning <= timestamp.hour <= end: #if payment was incoming and time is between specific chours
        data_output[timestamp_string] = [] # data_output={timestamp_string:{}}
        prices = requests.get("https://api.coindesk.com/v1/bpi/historical/close.json?start=" + timestamp_string[0:10] + "&end=" + timestamp_string[0:10]) #request historical price in format YYYY-MM-DD
        check_request(prices)
        prices_json = json.loads(prices.content) #load json
        bitcoins = satoshis / 100000000.0 #change satoshis to bitcoins
        details = requests.get("https://www.blockonomics.co/api/tx_detail?txid=" + i['txid']) #get details about specific transaction. get address etc txid = transaction id
        check_request(details)
        transactions_details = json.loads(details.content) #load json
        for j in transactions_details['vin']: #for every item in incoming payments
            income_address = j['address'] #get address which made a payment
            dollars = round(prices_json['bpi'][timestamp_string[0:10]] * bitcoins,2) #change to dollars


            wallet_details_request = requests.get("https://blockchain.info/rawaddr/" + j['address']) #get details about wallet, which made payment
            wallet_details_json = json.loads(wallet_details_request.content)

            #gather information about wallet
            wallet_info = {
                "Balance": wallet_details_json['final_balance'] / 100000000.0,
                "Received": wallet_details_json['total_received'] / 100000000.0,
                "Sent": wallet_details_json['total_sent'] / 100000000.0,
                "Transactions": len(wallet_details_json['txs']),
                "First transaction": datetime.datetime.fromtimestamp(
                (wallet_details_json['txs'][-1]['time'])),
                "Last transaction": datetime.datetime.fromtimestamp(
                (wallet_details_json['txs'][0]['time'])) }

            data_output[timestamp_string] = ({"BTC":bitcoins,
                                                  "USD": prices_json['bpi'][timestamp_string[0:10]] * bitcoins,
                                                  income_address: wallet_info})

            #PRINT
            balance = wallet_details_json['final_balance'] / 100000000.0
            print "Address " + colored(j['address'],'green')+ " transferred " + str(colored(bitcoins,'red')) + "(" + str(colored(dollars, 'green')) + colored("$",'green') + ") to " + colored((i['addr'][0]),'green') + " at " + colored(timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'red')
            print "More information about " + j['address']
            print "\tBalance:", colored(balance,"green") if balance > 0.0 else balance #wow
            print "\tReceived: ", wallet_details_json['total_received'] / 100000000.0
            print "\tSent:", wallet_details_json['total_sent'] / 100000000.0
            print "\tTransactions:", len(wallet_details_json['txs'])
            print "\tFirst transaction:", datetime.datetime.fromtimestamp(
                (wallet_details_json['txs'][-1]['time']))
            print "\tLast transaction:", datetime.datetime.fromtimestamp(
                (wallet_details_json['txs'][0]['time']))
            print("-------------------------------------------------------------")

        #json
        if json_output:
            to_json(i['addr'][0], data_output)
