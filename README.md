# WhatsTheHype

### Requirements

python3.9

pip install yfinance, pandas, numpy, matplotlib

#### MAC OS Permission

```
cd /Applications/Python\ 3.9/
./Install\ Certificates.command
```

### Setup Reddit Config

redditConfig.json
```
{
    "clientId": "",
    "secret": "",
    "username": "",
    "password": ""
}
```

### API Documentation Resources

https://github.com/pushshift/api
https://github.com/ranaroussi/yfinance
https://www.reddit.com/dev/api/

### Run

python3 main.py -t <ticker> -s <subreddit> -p <day/week/month/year/all>

-h help
-t ticker
-s subreddit
-p day/month/year/all

example:

python3 main.py -t TSLA -s wallstreetbets -p week

This will show how many times TSLA was mentioned on wallstreetbets the past week and compare with the past weeks market data
mentions include, link submissions, and comments
