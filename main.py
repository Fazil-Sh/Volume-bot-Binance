import asyncio
import json
import websockets, requests


class BinanceApi:
    def __init__(self, quantity_tracking_coins):
        self._list_coins = []
        self._multiplier_all = {}
        self.qty_track = quantity_tracking_coins
        if not self._list_coins:
             BinanceApi.get_top_coins(self)
             
        self._bool_dict_coins = {c: False for c in self._list_coins}


    def get_top_coins(self):
        shit_coin = ['USDCUSDT', 'FDUSDUSDT', 'EURUSDT', 'PAXGUSDT', 'TUSDUSDT', 'EURIUSDT', 'USDPUSDT', 'WBTCUSDT']

        response = requests.get("https://api.binance.com/api/v3/ticker/24hr")
        tickers = response.json()
        usdt_coins = [coin for coin in tickers if coin['symbol'].endswith('USDT') and coin['symbol'] not in shit_coin]  
        top_coins = sorted(usdt_coins, key=lambda x: float(x['quoteVolume']), reverse=True)[:self.qty_track]

        for coin in top_coins:
            coin['symbol'] = coin['symbol'].lower()
            self._list_coins.append(coin['symbol'])
            vol = float(coin['quoteVolume'])
            self.__multi_vol(vol, coin['symbol'])


    def __multi_vol(self, vol, symb):
        multi = self._multiplier_all

        if vol < 5_000_000:
              multi[symb] = 400000
        elif vol > 5_000_000 and vol < 10_000_000:
              multi[symb] = 550000 #55
        elif vol > 10_000_000 and vol < 25_000_000:
              multi[symb] = 750000 #75
        elif vol > 25_000_000 and vol < 50_000_000:
              multi[symb] = 600000 #90
        elif vol > 50_000_000 and vol < 100_000_000:
              multi[symb] = 1_200_000 #1_400_000
        elif vol > 100_000_000 and vol < 250_000_000:
              multi[symb] = 1_200_000 #2_400_000
        elif vol > 250_000_000 and vol < 500_000_000:
              multi[symb] = 2_200_000 #4_500_000
        elif vol > 500_000_000 and vol < 1_000_000_000:
              multi[symb] = 3_200_000 #12_500_000
        elif vol > 1_000_000_000 and vol < 1_500_000_000:
              multi[symb] = 10_500_000 #12_500_000
        elif vol > 1_500_000_000:
              multi[symb] = 15_500_000 #12_500_000
                      


async def binance_websocket():
     async with websockets.connect(uri) as websocket:
          while True:
            message = await websocket.recv()
            data = json.loads(message)
            symb = data['s'].lower()

            if data['k']['x']:
                  c._bool_dict_coins[i] = False

            if float(data['k']['q']) > c._multiplier_all[symb] and c._bool_dict_coins[symb] == False and not data['k']['x']:
               c._bool_dict_coins[symb] = True
               
               text = f"⚡*{data['s'][:-4].upper()}* volume increase!"
               params = {'text': text, "parse_mode": "Markdown"}
               requests.post(f"https://api.telegram.org/bot<YourToken>/SendMessage?chat_id=<Your_chatId>&text={text}", params=params)



if __name__ == '__main__':
    c = BinanceApi(5)
    c.get_top_coins()

    uri = "wss://stream.binance.com:9443/ws/btcusdt@kline_5m"
    for i in range(len(c._list_coins)):
                uri += ('/' + c._list_coins[i] + '@kline_5m')

    asyncio.run(binance_websocket())