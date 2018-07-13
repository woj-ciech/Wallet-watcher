# Wallet-watcher
Small script for retrieving incoming transactions based on provided hour period.
You have to pass address(es) of wallet(s), start hour, end hour and if you want to get json output.
Based on this data, script retrieves all incoming transaction to this wallet(s). Additionally, it gathers information about address which has transferred the money.

Background ---> https://medium.com/@woj_ciech/osint-investigation-based-on-gao-report-about-firearm-sales-in-dark-web-bitcoin-tracking-with-a0dcfa7d8daf

## Usage
```
python wallet-watcher.py -h

usage: wallet-watcher.py [-h] [--address ADDRESS] [--begin BEGIN] [--end END]
                         [--json]

optional arguments:
  -h, --help         show this help message and exit
  --address ADDRESS  Address(es) in format: "xxx, yyy", (default:
                     1Nhztc2zhxzqqhTYFUE6bJw9sJAwTu7yYF)
  --begin BEGIN      Hour from which to start (default: 9)
  --end END          Hour from which to end (default: 17)
  --json             JSON output. wallet_name.txt in current directory
                     (default: False)
```

```
wallet-watcher.py --address "1Bd8evxVYZLF6FVNQpUGuwvzgqvoMVK2Lx, 1Jc65vRz6qC3r9XmGpmoEGBKmDZXc9sfNv" --begin 7 --end 19 --json

Checking all transactions of 1Bd8evxVYZLF6FVNQpUGuwvzgqvoMVK2Lx, 1Jc65vRz6qC3r9XmGpmoEGBKmDZXc9sfNv from 9 to 17
JSON output: True
Address 15xYYaZR8rg7EHGTvw9wdNNafucBtLW1xq transferred 2.383(945.02$) to 1Jc65vRz6qC3r9XmGpmoEGBKmDZXc9sfNv at 2014-09-21 13:59:31
More information about 15xYYaZR8rg7EHGTvw9wdNNafucBtLW1xq
	Balance: 0.0
	Received:  76.55762386
	Sent: 76.55762386
	Transactions: 50
	First transaction: 2014-08-31 12:50:21
	Last transaction: 2014-09-24 02:11:09
-------------------------------------------------------------
Address 1C9wv9cceYrgLKDYokjkQJDR8eYcjfWbVi transferred 2.383(945.02$) to 1Jc65vRz6qC3r9XmGpmoEGBKmDZXc9sfNv at 2014-09-21 13:59:31
More information about 1C9wv9cceYrgLKDYokjkQJDR8eYcjfWbVi
	Balance: 0.0
	Received:  3.09187527
	Sent: 3.09187527
	Transactions: 29
	First transaction: 2014-09-05 05:21:52
	Last transaction: 2014-09-24 02:10:36
```
## Output
```
cat 1Jc65vRz6qC3r9XmGpmoEGBKmDZXc9sfNv.json
{
    "2014-09-18 13:12:05": {
        "1AppR4J58uiLWucxb2GnY73ZoJLqkQkJFh": {
            "Balance": 0.0, 
            "First transaction": "2014-09-08 09:46:49", 
            "Last transaction": "2014-09-24 02:11:43", 
            "Received": 10.5362, 
            "Sent": 10.5362, 
            "Transactions": 32
        }, 
        "BTC": 0.00710698, 
        "USD": 2.995303526612
    }, 
    "2014-09-21 13:59:31": {
        "15xYYaZR8rg7EHGTvw9wdNNafucBtLW1xq": {
            "Balance": 0.0, 
            "First transaction": "2014-08-31 12:50:21", 
            "Last transaction": "2014-09-24 02:11:09", 
            "Received": 76.55762386, 
            "Sent": 76.55762386, 
            "Transactions": 50
        }, 
        "BTC": 2.383, 
        "USD": 945.019161
    }
```

## Additional
It uses three different API (Blockonomics.io, Coindesk.com and blockchain.com) but no keys are needed. All prices are also in USD in time of being transferred. Coindesk API was used to retrieve historical exchanges prices.

There is a lot to develop further, lots of different filters can be implemented. Feel free to use it and contribute.

Wallets in example are totally random.
