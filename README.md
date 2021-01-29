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

python3 main.py -t <ticker> -s <subreddit> -p <day/week/month/quarter/half/year> -o <posts/comments/all>

- -h (help)
- -t ticker
- -s subreddit
- -p day/week/month/year
- -c ./reddit/config/location
- -o posts/comments/all
- -v (verbose) prints dataframe info

example:

python3 main.py -t TSLA -s wallstreetbets -p week -o all

This will show how many times TSLA was mentioned on wallstreetbets (posts and comments) the past week and compare with the past weeks market data

- Since we can only get 100 comments at a time, searches with a bigger period will take a long time
- Use -v to see progress statements

### Examples

TODO

### Issues

- The charts are only as good as the data we have available. 
- Sometimes the pushshift comments for the current day are not all available

### TODO

- Currently this project is just a way to aggregate data
- I would like to expand this into the ability to discover new tickers that are trending upwards in mentions
- Comparing with market past market data it could be an interesting take on what makes market buzz
- Can also compare different subreddits and see which ones catch on faster

- Rights now comments vastly overpower posts, making the 'all' operation too similar to comments
- A possible soluution is weighing scores more, limited mentions to a link_id...
- Likewise, Average Score means less for comments, when there is a lot... need a better measure