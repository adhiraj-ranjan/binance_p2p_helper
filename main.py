import requests
import time
from tabulate import tabulate
from tqdm import tqdm

baseMoney_ = map(int, input("enter amount (separated by spaces) : ").split())

baseCoin = "USDT"
otherCoins = ["BTC", "BUSD", "BNB", "ETH", "ADA", "TRX", "SHIB", "MATIC", "WRX", "XRP", "SOL"]

tableHead = ["Coin", "Through", "To", "Profit", "Quote"]

def get_ad_quote(coin, tradeType, ad_num):
    json_data = {
    'page': 1,
    'rows': 10,
    'payTypes': [],
    'countries': [],
    'publisherType': None,
    'asset': coin,
    'fiat': 'INR',
    'tradeType': tradeType,
}

    response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', json=json_data)
    try:
        response_req_quote = response.json()['data'][ad_num-1]['adv']['price']
    except:
        print(response.json())
        sleep_(2)
        return get_ad_quote(coin, tradeType, ad_num)

    return response_req_quote

def convert(from_, to_, amount_):
    json_data = {
        'fromCoin': from_,
        'requestAmount': amount_,
        'requestCoin': from_,
        'toCoin': to_,
        'walletType': 'FUNDING',
    }

    response = requests.post('https://www.binance.com/bapi/margin/v1/private/new-otc/get-quote', cookies="", headers="", json=json_data)
    try:
        req_ = response.json()['data']['toCoinAmount']
    except:
        if response.json()['message'] == "Failed to get quote":
            sleep_()
            pass
        else:
            print(response.json())
            sleep_(2)
        return convert(from_, to_, round(amount_, 2))
        
    return req_

def convert_tousdt(from_, amount_):
    response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={from_}USDT")
    req_ = float(response.json()['price']) * amount_
    return req_


def get_ad_by_amount(coin, amount, tradeType="BUY"):
    json_data = {
    'page': 1,
    'rows': 10,
    'payTypes': [],
    'countries': [],
    'publisherType': None,
    'transAmount': amount,
    'asset': coin,
    'fiat': 'INR',
    'tradeType': tradeType,
    }

    response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', json=json_data)
    try:
        response_req_quote = response.json()['data'][0]['adv']['price']
        response_req_name = response.json()['data'][0]['advertiser']['nickName']
    except:
        print(response.json())
        sleep_(2)
        return get_ad_by_amount(coin, amount, tradeType)
    return response_req_quote, response_req_name

def sleep_(t=1):
    time.sleep(t)

base_quote = get_ad_quote(coin=baseCoin, tradeType="BUY", ad_num=5)



for baseMoney in baseMoney_:
    profit_data = []
    print(f"# CALCULATING FOR INR {baseMoney}")
    
    '''
    for coin in tqdm(otherCoins):
        quote = get_ad_quote(coin=coin, tradeType="SELL", ad_num=1)
        c_amount = (baseMoney/float(quote))

        base_amount = convert(from_=coin, to_=baseCoin, amount_=round(c_amount, 8))

        profit_amount = (float(base_amount) * float(base_quote)) - baseMoney
        
        if profit_amount > 50:
            r_list = [coin, "ads", baseCoin, round(profit_amount, 0), str(quote)]
            profit_data.append(r_list)
        
        sleep_()
    '''
    for coin in tqdm(otherCoins):
        quote, nickname = get_ad_by_amount(coin=coin, amount=baseMoney)
        c_amount = (baseMoney/float(quote))

        base_amount = convert_tousdt(from_=coin, amount_=round(c_amount, 8))

        profit_amount = (float(base_amount) * float(base_quote)) - baseMoney
        
        if profit_amount > 25:
            r_list = [coin, nickname, baseCoin, round(profit_amount, 0), str(quote)]
            profit_data.append(r_list)

    for coin in tqdm(otherCoins):
        b_amount = (baseMoney/float(base_quote))
        
        usdt_per_coin = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT").json()['price']
        coin_per_usdt = (1/float(usdt_per_coin))
        coinAmountForBamount = coin_per_usdt * b_amount

        quote, nickname = get_ad_by_amount(coin=coin, amount=baseMoney, tradeType="SELL")

        # base_amount = convert_tousdt(from_=coin, amount_=round(c_amount, 8))

        profit_amount = (coinAmountForBamount * float(quote)) - baseMoney
        
        if profit_amount > 25:
            r_list = [baseCoin, coin, nickname, round(profit_amount, 0), str(quote)]
            profit_data.append(r_list)

    print(tabulate(profit_data, headers=tableHead, tablefmt="grid"))
