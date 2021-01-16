from binance.client import Client
from binance.websockets import BinanceSocketManager
import os
import time

api_key = "INSERT_API_KEY_HERE"
secret_key = "INSERT_SECRET_KEY_HERE"
client = Client(api_key, secret_key)

class bcolors:
	WARNING = '\033[91m'
	ENDC = '\033[0m'

selected_coin = "TRX"
margin = 0.005
sleep_time = 0.0

books = []
books_list = []
count = 0
arbitrage = 0
start_time = time.time()

def handle_info(msg):
	global books, books_list, margin, count, selected_coin, arbitrage
	data = msg["data"]
	time.sleep(sleep_time)
	os.system("clear")
	runtime = round(time.time() - start_time, 2)
	print("time: " + str(runtime) + "	updates: " + str(count) + "	ratio: " + str(round(float(count) / runtime, 2)) + "	arbitrage: " + str(arbitrage) + "\n")
	count = count + 1
	if (not next((item for item in books if item["s"] == data["s"]), False)):
		books_list.append(data["s"])
		books_list = sorted(books_list)
		books.insert(next(i for i in range(len(books_list)) if data["s"] == books_list[i]), data)
	else:
		for i in range(len(books)):
			if (books[i]["s"] == data["s"]):
				books[i] = data;
			i = i + 1
		for item in books:
			if item["s"][0:len(selected_coin)] == selected_coin:
				print(item["s"] + ":")
				if item["s"][-4:] != "USDT":
					fiat_symbol = item["s"][-(len(item["s"]) - len(selected_coin)):] + "USDT"
					fiat_price = float(next((fiat["a"] for fiat in books if fiat["s"] == fiat_symbol), 0.0))
					print("bid: " + item["b"] + "	USDT: " + str(fiat_price * float(item["b"])) + "\nask: " + item["a"] + "	USDT: " + str(fiat_price * float(item["a"])) + "\n")
					fiat_ask = fiat_price * float(item["a"])
					if fiat_ask == 0:
						fiat_ask = -1
					if (not next((item for item in books if item["s"] == selected_coin + "USDT"), False)):
						coin_price = fiat_ask
					else:
						coin_price = float(books[next(i for i in range(len(books)) if books[i]["s"] == selected_coin + "USDT")]["a"])
					diff = ((coin_price / fiat_ask) if fiat_ask < coin_price else (fiat_ask / coin_price))
					if diff > 1.0 + margin and fiat_ask > 0:
						print(f"{bcolors.WARNING}ARBITRAGE{bcolors.ENDC}\n")
						arbitrage = arbitrage + 1
				else:
					print("bid: " + item["b"] + "\nask: " + item["a"] + "\n")
	
bsm = BinanceSocketManager(client)
conn_key = bsm.start_multiplex_socket([selected_coin.lower() + 'usdt@bookTicker',
selected_coin.lower() + 'eth@bookTicker', selected_coin.lower() + 'btc@bookTicker',
'ethusdt@bookTicker', 'btcusdt@bookTicker'], handle_info)
bsm.start()
