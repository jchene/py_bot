import os
import time
from binance.client import Client
from binance.websockets import BinanceSocketManager

class bcolors:
	WARNING	= '\033[91m'
	ENDC	= '\033[0m'

target = "TRX"
margin = 0.005
slp_time = 0.1

books, books_idx = [], []
count, arbitrage = 0, 0
start_time = time.time()

def get_keys():
	key = ["", ""]
	for i in range(2):
		path = "../../api/" + input("Input api key file name: ")
		if os.path.isfile(path):
			File = open(path, "r")
			key[i] = File.read()[:-1]
			File.close()
		else:
			print("Missing file \"" + path + "\" exiting...")
			time.sleep(2)
			exit()
	return (key[0], key[1])

def update_display():
	global start_time, count, arbitrage, books, books_idx
	runtime = round(time.time() - start_time, 2)
	print("time: " + str(runtime) + "	updates: " + str(count) + \
		"	ratio: " + str(round(float(count) / runtime, 2)) + \
		"	arbitrage: " + str(arbitrage) + "\n")
	print(books_idx)

def handle_info(msg):
	global count, slp_time, books, books_idx
	count += 1
	time.sleep(slp_time)
	os.system("clear")
	data = msg["data"]
	if (not next((item for item in books if item["s"] == data["s"]), False)):
		books_idx.append(data["s"])
		books_idx = sorted(books_idx)
		books.insert(next(i for i in range(len(books_idx)) if data["s"] == books_idx[i]), data)
	else:
		for i in range(len(books)):
			if (books[i]["s"] == data["s"]):
				books[i] = data;
			i = i + 1
	update_display()

def main():
	global books, books_idx
	os.system("clear")
	api_key, secret_key = get_keys()
	client = Client(api_key, secret_key)
	bsm = BinanceSocketManager(client)
	conn_key = bsm.start_multiplex_socket([target.lower() + 'usdt@bookTicker',
	target.lower() + 'eth@bookTicker', target.lower() + 'btc@bookTicker',
	'ethusdt@bookTicker', 'btcusdt@bookTicker'], handle_info)
	bsm.start()

if __name__ == "__main__":
	main()
