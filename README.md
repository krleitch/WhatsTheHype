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

- https://github.com/pushshift/api
- https://github.com/ranaroussi/yfinance
- https://www.reddit.com/dev/api/

### Run

python3 main.py -t <ticker> -s <subreddit> -p <day/week/month/year/all>

- -h (help)
- -t ticker
- -s subreddit
- -p day/month/year/all
- -c ./reddit/config/location

example:

python3 main.py -t TSLA -s wallstreetbets -p week

This will show how many times TSLA was mentioned on wallstreetbets (posts and comments) the past week and compare with the past weeks market data

### Examples

TODO

### TODO

- Currently this project is just a way to aggregate data
- I would like to expand this into the ability to discover new tickers that are trending upwards in mentions
- Comparing with market past market data it could be an interesting take on what makes market buzz
- Can also compare different subreddits and see which ones catch on faster