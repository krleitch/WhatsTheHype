# WhatsTheHype

## Table of Contents
1. [Setup And Requirements](#setup-and-requirements)
2. [Running WhatsTheHype](#running-whatsthehype)
3. [Findings](#findings)
3. [API Resources](#api-resources)
4. [Known Issues](#knwon-issues)
5. [Future Plans](#future-plans)

## Setup and Requirements

- python3.9
- pip install yfinance, pandas, numpy, matplotlib

### MAC OS Permission

```
cd /Applications/Python\ 3.9/
./Install\ Certificates.command
```

### Create Reddit Config

- Place redditConfig.json in main folder
- you can also you -c to specify anotherr config location

redditConfig.json
```
{
    "clientId": "",
    "secret": "",
    "username": "",
    "password": ""
}
```

## Running WhatsTheHype

python3 main.py -t ticker -s subreddit -p day/week/biweek/month/quarter/half/year -o links/comments/all -v

\* arguments are required

- -h (help) prints help message
- -c (config) ./reddit/config/location
- -t* ticker
- -s* subreddit (do not include r/)
- -p* (period) one of day/week/biweek/month/quarter/half/year
- -o* (operation) one of links/comments/all
- -v (verbose) prints dataframe info

Example:

python3 main.py -t TSLA -s wallstreetbets -p week -o all

This will show how many times TSLA was mentioned on wallstreetbets (links and comments) the past week and compare with the past weeks market data

### Important Notes

- Since we can only get 100 comments at a time due to api restrictions, searches with a bigger period will take a long time
- Use -v to see progress statements and print the dataframes when finished

## Findings

TODO

## API Resources

- https://github.com/pushshift/api (used for comments)
- https://github.com/ranaroussi/yfinance (used for tickers)
- https://www.reddit.com/dev/api/ (used for links)

## Known Issues

- The charts are only as good as the data available. Sometimes pushshift comments for the current orr previous day are not available at the time of running  giving skewing results

## Future Plans

- Currently this project is just a way to aggregate and display data
- I would like to expand this into the ability to discover new tickers that are trending upwards in mentions
- Comparing with past market data it could be an interesting take on what makes market buzz
- Can also compare different subreddits and see which ones catch on faster

### Planned Changes

- Rights now comments vastly overpower links, making the 'all' operation too similar to comments
- A possible soluution is weighing scores more, limited mentions to a link_id...
- Likewise, Average Score means less for comments, when there are so many... a better measure is needed... (weight number of replies or discussion)