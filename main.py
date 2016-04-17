import requests
import config
import hashlib,hmac
import time
import json
import urllib

def getCryptoPrice(only):
	data = requests.get("https://poloniex.com/public?command=returnTicker").json()
	prices = {}
	
	for i in only:
		try:
			prices[i] = data["BTC_"+i]["highestBid"]
		except:
			pass
	return prices		


def getPoloBal():

	value = {
		"command": "returnBalances",
		"nonce": int(time.time() * 10000)
	}

	headers = {
		"Key": config.polo["Key"],
		"Sign": hmac.new(config.polo["Secret"], urllib.urlencode(value), hashlib.sha512).hexdigest()
	}

	data = requests.post("https://poloniex.com/tradingApi",headers=headers,data=value).json()

	return data

def displayCrypto():
	total = 0
	prices = getCryptoPrice(config.crypto)
	print("||||CRYPTO||||")	

	for i in prices:
		currentValue = round(float(prices[i]) * config.crypto[i]["amount"],8)
		boughtValue = round(config.crypto[i]["amount"] * config.crypto[i]["rate"],8)
		pl = round(((currentValue - boughtValue) / currentValue ) * 100,2) 
	
		print("[%s] - [Holdings : %f] - [Rate : %s] - [BTC value : %f] - [Profit/Loss : %f%%]"
			 %(i,config.crypto[i]["amount"],prices[i],currentValue,pl))
		total += currentValue

	print("")

	data = getPoloBal()
	prices = getCryptoPrice(data)

	if config.polo["Key"] :
		print("||||POLONIEX||||")
	
		for i in prices:
			if float(data[i]) > 0:		
				currentValue = round(float(prices[i]) * float(data[i]),8)
				print("[%s] - [Holdings : %f] - [Rate : %s] - [BTC value : %f]"
					%(i,float(data[i]),prices[i],currentValue))
				total += currentValue

		print("")

	print("Total in BTC : %fBTC" %(total))
displayCrypto()
