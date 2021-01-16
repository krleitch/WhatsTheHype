# WhatsTheHype

### Requirements

python3.X

pip install yfinance, pandas, numpy, matplotlib

#### MAC OS Permission

```
cd /Applications/Python\ 3.X/
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

### Run

python3 main.py -t <ticker> -s <subreddit> -p <period>

-h help
-t ticker
-s subreddit
-d day/month/year/all

example:

python3 main.py 'TSLA' 'wallstreetbets' 'week'

This will show how many times TSLA was mentioned on wallstreetbets the past week and compare with the past weeks market data
mentions include, link submissions, and comments
