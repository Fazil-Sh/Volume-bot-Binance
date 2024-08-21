# How the bot works:
1) Parses the top coins by trading volume
2) Counts the trading volume for each coin

# How to use:  
Pass in a class instance of the number of coins to track
For example: 
```python
bot = BinanceApi(5)
```
Here the bot will track the top 5 coins by trading volume.  
  
Don't forget `token, chat_id` for telegram  

# Contributing
```Fork this Repo
Commit your changes (git commit -m 'Add some feature')
Push to the changes (git push)  
Create a new Pull Request  
Thanks all for your contributions...
