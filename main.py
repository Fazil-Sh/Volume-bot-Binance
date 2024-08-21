import asyncio
import json
import websockets, requests


class BinanceApi:
    def __init__(self, quantity_tracking_coins):
        self._list_coins = []
        self._multiplier_all = {}
        self.qty_track = quantity_tracking_coins


    def get_top_coins(self):
        shit_coin = ['USDCUSDT', 'FDUSDUSDT', 'EURUSDT', 'PAXGUSDT', 'TUSDUSDT']

        response = requests.get("https://api.binance.com/api/v3/ticker/24hr")
        tickers = response.json()
        usdt_coins = [coin for coin in tickers if coin['symbol'].endswith('USDT') and coin['symbol'] not in shit_coin]  
        top_coins = sorted(usdt_coins, key=lambda x: float(x['quoteVolume']), reverse=True)[:self.qty_track]

        for coin in top_coins:
            coin['symbol'] = coin['symbol'].lower()
            self._list_coins.append(coin['symbol'])
            vol = float(coin['quoteVolume'])
            multi = self._multiplier_all
            print(coin['symbol'], coin['quoteVolume'])

            if vol < 50_000_000:
                 multi[coin['symbol']] = 5
            elif vol > 50_000_000 and vol < 100_000_000:
                  multi[coin['symbol']] = 4.5
            elif vol > 100_000_000 and vol < 500_000_000:
                  multi[coin['symbol']] = 3.2
            elif vol > 500_000_000 and vol < 1_000_000_000:
                  multi[coin['symbol']] = 2.8
            elif vol > 1_000_000_000 and vol < 1_500_000_000:
                  multi[coin['symbol']] = 2.5
            elif vol > 1_500_000_000:
                  multi[coin['symbol']] = 2.2
                      
        self._bool_dict_coins = {c: False for c in self._list_coins}
        self._Vol_100candle_30min = {c: 0 for c in self._list_coins}
        self._correct_vol_altcoin = {c: 0 for c in self._list_coins}
        self._all_volume = {c: 0 for c in self._list_coins}
        


    def get_vol_100candles_30m(self):
        list_coins = self._list_coins
        correct_vol = self._correct_vol_altcoin

        for i in range(len(list_coins)):
            params = {
                 'symbol': list_coins[i].upper(),  
                 'interval': '30m',     
                 'limit': 100}
            ticker = requests.get('https://api.binance.com/api/v3/klines', params = params).json()
            for i1 in range(len(ticker)):
                 self._Vol_100candle_30min[list_coins[i]]+=float(ticker[i1][5])

        for b in range(len(list_coins)):
            correct_vol[list_coins[b]] = round(self._Vol_100candle_30min[list_coins[b]] * (self._multiplier_all[list_coins[b]] / 100))
                 


async def binance_websocket():
     async with websockets.connect(uri) as websocket:
          while True:
            message = await websocket.recv()
            data = json.loads(message)
            data['s'] = data['s'].lower()

            if data['e'] == 'aggTrade':
                 c._all_volume[data['s']] += float(data["q"])

                 if c._all_volume[data['s']] >= c._correct_vol_altcoin[data["s"]] and not c._bool_dict_coins[data['s']]:
                     c._bool_dict_coins[data['s']] = True
                     text = f"volume increase!!!\n - {data['s'][:-4]}"
                     params = {'text': text}
                     requests.post(f"https://api.telegram.org/bot<YourToken>/SendMessage?chat_id=<Your_chatId>&text={text}", params=params)

            if data['e'] == 'kline' and data['k']['x']:
                 for i, i2 in zip(c._bool_dict_coins.keys(), c._all_volume.keys()):
                      c._bool_dict_coins[i] = False
                      c._all_volume[i2] = 0


if __name__ == '__main__':
    c = BinanceApi(12)
    c.get_top_coins()
    c.get_vol_100candles_30m()

    uri = "wss://stream.binance.com:9443/ws/btcusdt@kline_5m"
    for i in range(len(c._list_coins)):
                uri += ('/' + c._list_coins[i] + '@aggTrade')

    asyncio.run(binance_websocket())