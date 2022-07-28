# binance_p2p_helper
Script to Scrape Binance P2P ads Data and Calculate Easy Profit Opportunity

Note - Runs on **`python3`**

### Install Dependencies
- requests
- tabulate

### Usage
On running the script **`python main.py`**, Enter amount (from which you want to trade with/find opportunity with) separated by spaces for multiple searches at once.
It will fetch Current Market Prices, and Respective Ad Quotes, and Shows the profitable data in tabular form.

### How It Works
1) Here the Base asset is taken as USDT
2) Two Algorithms Are Used: 
    - Upon Buying an asset from specified Ad, and Converting to USDT and selling it throught Ads gives profit, returns Profit
    - On Buying USDT from Ad at good price, Converting it to Specified Asset and selling it to specified User, return Profit
 
### Things to keep nder consideration
1) Crypto prices are very volatile
2) Calculated profit at current can change to loss the other second

NOTE - Most of the time, table data might be empty, this just means there is no easy opportunity.

