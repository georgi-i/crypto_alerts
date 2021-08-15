from binance.client import Client
import time
from pyfiglet import figlet_format
import logging
import ctypes
import os

logging.basicConfig(filename='crypto_alerts.log', 
                    format='%(asctime)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S', 
                    level=logging.INFO)

welcome = figlet_format("Hello", font = "isometric1")
print(welcome)

# Binance account API key and secret
api_key = ''
api_secret = ''

client = Client(api_key, api_secret)

def get_prices(symbols):
        prices = []
        for symbol in symbols:
                tickers = client.get_ticker(symbol = symbol)
                prices.append(float(tickers['lastPrice']))
        
        return prices

def beep():
        print('\a')

def add_prices_to_queue(requests_counter, prices_queue, symbols):
        prices_queue.append(get_prices(symbols))
        requests_counter += 10

def update_prices_queue(requests_counter, prices_queue, symbols, update_index):
        prices_queue[update_index] = get_prices(symbols)
        requests_counter += 10

def check_for_green_candles(current_prices, prices_queue, symbols):
        
        index = 0                                                   
        for (price, price_q) in zip(current_prices, prices_queue):

                # Check for +10%
                if price >= (price_q * 1.1):
            
                        current_time = time.time() - start_time
                        beep()
                        print('  <-------------------A L E R T----------------------------->\n')
                        alert_message = f'   The price of {symbols[index]} has risen with 10% for {current_time / 60} minutes!\n'
                        logging.info(alert_message)
                        print(alert_message)
                        print('  <-------------------A L E R T----------------------------->\n')
                        beep()
                        
                        # Message box pop-up on Windows OS
                        if os.name == 'nt':
                                ctypes.windll.user32.MessageBoxW(0, alert_message, 'ALERT', 1)
            
                if index == 0:
                        print('\n')
                        print('   |---------------------------------|\n')
                        print('   |       Current prices are:       |\n')
                        print('   |---------------------------------|\n')
        
                current_price_message = f'   The price of {symbols[index]} is {price}.\n'
                logging.info(current_price_message)
                print(current_price_message)

                index += 1


symbols = [ 'DOGEUSDT',     #0
            'ETCUSDT', 
            'BCHUSDT', 
            'SCUSDT', 
            'LTCUSDT', 
            'THETAUSDT', 
            'EOSUSDT', 
            'FILUSDT', 
            'TRXUSDT',
            'USDTNGN',
            'ETHUSDT']     #10


print('   Script started...')
print('   Awaiting request response...')
logging.info('Script started\n')

start_time = time.time()

#queue for storing prices at execution and every around 60 seconds
prices_queue = []
requests_counter = 0
add_prices_to_queue(requests_counter, prices_queue, symbols)

update_index = 0 

while True:

        current_prices = get_prices(symbols)
        requests_counter += 10

        current_minutes = (time.time() - start_time) / 60

        if len(prices_queue) != 11:
                if current_minutes >= 10:
                        add_prices_to_queue(requests_counter, prices_queue, symbols)
                elif  current_minutes >= 9:
                        add_prices_to_queue(requests_counter, prices_queue, symbols)
                elif current_minutes >= 8:
                        add_prices_to_queue(requests_counter, prices_queue, symbols)
                elif current_minutes >= 7:
                        add_prices_to_queue(requests_counter, prices_queue, symbols)
                elif current_minutes >= 6:
                        add_prices_to_queue(requests_counter, prices_queue, symbols)
                elif current_minutes >= 5:
                        add_prices_to_queue(requests_counter, prices_queue, symbols)
                elif current_minutes >= 4:
                        add_prices_to_queue(requests_counter, prices_queue, symbols)
                elif current_minutes >= 3:
                        add_prices_to_queue(requests_counter, prices_queue, symbols)
                elif current_minutes >= 2:
                        add_prices_to_queue(requests_counter, prices_queue, symbols)
                elif current_minutes >= 1:
                        add_prices_to_queue(requests_counter, prices_queue, symbols)
        else:
                update_prices_queue(requests_counter, prices_queue, symbols, update_index)
                update_index += 1
                if update_index == 12:
                        update_index = 0

       
        check_for_green_candles(current_prices, prices_queue[0], symbols)

        try:
                check_for_green_candles(current_prices, prices_queue[1], symbols)
                check_for_green_candles(current_prices, prices_queue[2], symbols)
                check_for_green_candles(current_prices, prices_queue[3], symbols)
                check_for_green_candles(current_prices, prices_queue[4], symbols)
                check_for_green_candles(current_prices, prices_queue[5], symbols)
                check_for_green_candles(current_prices, prices_queue[6], symbols)
                check_for_green_candles(current_prices, prices_queue[7], symbols)
                check_for_green_candles(current_prices, prices_queue[8], symbols)
                check_for_green_candles(current_prices, prices_queue[9], symbols)
                check_for_green_candles(current_prices, prices_queue[10], symbols)
        
        except IndexError:
                pass
                
    
        print('   /---------------------------------\\')
        print(f'         Current requests are: {requests_counter}')
        print('   \\---------------------------------/\n')


        print('   Logging data to file: crypto_alerts.log\n')
        print(f'   Current minutes are: {current_minutes:.2f}\n')
        print('   Sleeping for 4 seconds...')
        time.sleep(4)

