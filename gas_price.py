#!/usr/bin/python3.7
import json
import sys
import requests

convert = 1e18 # 1000000000000000000
baseurl = 'https://api.etherscan.io/api?module='
modgas = 'gastracker&action='
address = 'address='
tag = '&tag=latest&'
apikey = 'apikey='
eth_amount = []
balance = ()
gasinfo = {}

with open("user.json") as u:
    user = json.load(u)
    # TODO if apiKey etherscan not in JSON: exit()
    apikey += user["apikeys"]["etherscan"]
    for i in user["ethereum"]:
        json_dump = json.dumps(i)
        json_object = json.loads(json_dump)
    

def buildmetric():
    gasfee = gas_price()
    original_stdout = sys.stdout # Save a reference to the original standard output

    with open('eth-net-metrics.prom', 'w') as f:
            sys.stdout = f # Change the standard output to the file we created.

            print('# HELP etherscan_blockheight Block No. via etherscan.')                                
            print('# TYPE etherscan_blockheight counter')
            print('etherscan_blockheight{block="height"} ',gasfee['LastBlock'],sep='')
            print('# HELP etherscan_gas Gas Price Safe, Proposed and Fast fetched via etherscan.')
            print('# TYPE etherscan_gas gauge')
            print('etherscan_gas{block="',gasfee['LastBlock'],'", speed="slow"} ',gasfee["SafeGasPrice"],sep='')
            print('etherscan_gas{block="',gasfee['LastBlock'],'", speed="slow"} ',gasfee["SafeGasPrice"],sep='')
            print('etherscan_gas{block="',gasfee["LastBlock"],'", speed="medium"} ',gasfee["ProposeGasPrice"],sep='')
            print('etherscan_gas{block="',gasfee["LastBlock"],'", speed="fast"} ',gasfee["FastGasPrice"],sep='')
            sys.stdout = original_stdout # Reset the standard output to its original value


def gas_price():
    gasinfo = {}
    action = 'gasoracle&'
    res = requests.get(baseurl+modgas+action+apikey).json()
    if res['status'] == str(0):
        sys.exit("Invalid API-Key")
    json_dump = json.dumps(res)
    
    json_object = json.loads(json_dump)
    gasinfo = (json_object["result"])
    return(gasinfo)

buildmetric()