#!/usr/bin/python3.7
import json
import sys
import requests

convert = 1e18 # 1000000000000000000
baseurl = 'https://api.etherscan.io/api?module='
modaccount = 'account&action='
modgas = 'gastracker&action='
address = 'address='
tag = '&tag=latest&'
apikey = 'apikey='
eth_amount = []
balance = ()
gasinfo = {}
wallets = {}
tokens = {}
pools = {}


with open("user.json") as u:
    user = json.load(u)
    # TODO if apiKey etherscan not in JSON: exit()
    apikey += user["apikeys"]["etherscan"]
    for i in user["ethereum"]:
        json_dump = json.dumps(i)
        json_object = json.loads(json_dump)
        wallets[json_object["name"]] = json_object["address"]
        # TODO if tokens available in JSON, push them to tokens
        tokens[json_object["name"]] = json_object["tokens"]
        pools[json_object["name"]] = json_object["pools"]


def pytherium():
    myeth = eth_balance()
    mytokens =  get_tokens()
    mypools = get_unipools()

    original_stdout = sys.stdout # Save a reference to the original standard output
  
    with open('eth-balance-metrics.prom', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print('# HELP etherscan_wallet_main Balance of eth wallet fetched via etherscan.')
        print('# TYPE etherscan_wallet_main gauge')
        print('etherscan_wallet_main{wallet=','"',wallets["ACCOUNT-NAME"],'", ','name="ETH"',', ','type="coin"}',' ',myeth['ACCOUNT-NAME'],sep='')
        print('etherscan_wallet_main{wallet=','"',wallets['ACCOUNT-NAME'],'", ','name="WBTC"',', ','type="token"}',' ',mytokens["WBTC"],sep='')
        print('etherscan_wallet_main{wallet=','"',wallets['ACCOUNT-NAME'],'", ','name="UNI"',', ','type="token"}',' ',mytokens["UNI"],sep='')
        print('etherscan_wallet_main{wallet=','"',wallets['ACCOUNT-NAME'],'", ','name="DAI"',', ','type="token"}',' ',mytokens["DAI"],sep='')
        print('etherscan_wallet_main{wallet=','"',wallets['ACCOUNT-NAME'],'", ','name="DPI"',', ','type="token"}',' ',mytokens["DPI"],sep='')
        print('etherscan_wallet_main{wallet=','"',wallets['ACCOUNT-NAME'],'", ','poolname="WBTC"',', ','type="pool"}',' ',mypools["WBTC"],sep='')
        print('etherscan_wallet_main{wallet=','"',wallets['ACCOUNT-NAME'],'", ','poolname="UNI"',', ','type="pool"}',' ',mypools["UNI"],sep='')
        print('etherscan_wallet_main{wallet=','"',wallets['ACCOUNT-NAME'],'", ','poolname="CRV"',', ','type="pool"}',' ',mypools["CRV"],sep='')

        sys.stdout = original_stdout # Reset the standard output to its original value


def eth_balance():
    action = 'balance&'
    balances = {}
    for name, wallet in wallets.items():
        res = requests.get(baseurl+modaccount+action+wallet+"&"+address+wallet+tag+apikey).json()
        json_dump = json.dumps(res, sort_keys = True, indent = 4)
        print(res)
        json_object = json.loads(json_dump)
        reswai = (json_object["result"])
        amounts = int(reswai)/convert
        balances[name] = amounts
        balance = (balances)
    return(balance)

def get_tokens():
    action = 'tokenbalance&contractaddress='
    amounts = {}
    for walletName, walletId in wallets.items():
      for token in tokens[walletName]:
          res = requests.get(baseurl+modaccount+action+(token["address"])+"&"+address+walletId+tag+apikey).json()
          json_dump = json.dumps(res, sort_keys = True, indent = 4)
          print(res)
          json_object = json.loads(json_dump)        
          reswai = json_object["result"]
          amounts[token["tokenname"]] = int(reswai)/convert
    return(amounts)

def get_unipools():
    action = 'tokenbalance&contractaddress='
    amounts = {}
    for walletName, walletId in wallets.items():
      for poolContract in pools[walletName]:
          res = requests.get(baseurl+modaccount+action+(poolContract["address"])+"&"+address+walletId+tag+apikey).json()
          json_dump = json.dumps(res, sort_keys = True, indent = 4)
          print(res)
          json_object = json.loads(json_dump)
          reswai = json_object["result"]
          amounts[poolContract["poolname"]] = int(reswai)/convert
    return(amounts)


pytherium() 
