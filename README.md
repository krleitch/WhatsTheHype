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

- Place redditConfig.json in main folder.
- you can also use -c to specify another config location.

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

```
python3 main.py -t ticker -s subreddit -b #days -a #days -o links/comments/all -v
```

\* arguments are required

- -h (help) prints help message
- -c (config) ./reddit/config/location
- -t* ticker
- -s* subreddit (do not include r/)
- -b* (before) only give items before this # of days ago
- -a* (after) only give items after this # of days ago
- -o* (operation) one of links/comments/all
- -v (verbose) prints dataframe info

Example:

```
python3 main.py -t tsla -s wallstreetbets -b 1 -a 8 -o all
```

This will show how many times TSLA was mentioned on wallstreetbets (links and comments) after 8 days ago but before 1 day ago then comparing with the past weeks market data.

Types of Charts:

- For large data sets (currently >= 50). The Moving Average with 25 data points is shown for mentions and scores. This is because we are more focused on the trend which is easier to see with the MA than with the large amount of data points.
- For small sets ( curently <= 15 ) individual data markers are set.
- The parameters for these can be found in graphingClient.py if you ever need to change or remove them. In The future there will be options to change chart types from the command line.

### Important Notes

- Since we can only get 100 comments at a time due to api restrictions, searches with a bigger after - before range will take a long time.
- A before of 0 for comments is not advised since we normally have incomplete comment data for the current day.
- Use -v to see progress info and print the dataframes when finished.

## Findings

It is important not to read too much into any of the data at this point, but here are some interesting findings

### Arguments: -t gme -s wallstreetbets -b 1 -a 15 -o links

![gme-biweek-links](https://github.com/krleitch/WhatsTheHype/blob/main/examples/gme-biweek-links.png)

### Arguments: -t gme -s wallstreetbets -b 1 -a 30 -o links

![gme-wallstreetbets-links-month](https://github.com/krleitch/WhatsTheHype/blob/main/examples/gme-wallstreetbets-links-month.png)

### Arguments: -t spy -s personalfinance -b 1 -a 365 -o all

![spy-personalfinance-all-year](https://github.com/krleitch/WhatsTheHype/blob/main/examples/spy-personalfinance-all-year.png)

### Arguments: -t tsla -s personalfinance -b 1 -a 365 -o all

![tsla-personalfinance-all-year](https://github.com/krleitch/WhatsTheHype/blob/main/examples/tsla-personalfinance-all-year.png)

### Arguments: -t tsla -s stocks -b 1 -a 365 -o all

![tsla-stocks-all-year](https://github.com/krleitch/WhatsTheHype/blob/main/examples/tsla-stocks-all-year.png)

### Arguments: -t tsla -s wallstreetbets -b 1 -a 365 -o all

![tsla-wallstreetbets-all-365](https://github.com/krleitch/WhatsTheHype/blob/main/examples/tsla-wallstreetbets-all-365.png)

## API Resources

- https://github.com/pushshift/api (used for comments)
- https://github.com/ranaroussi/yfinance (used for tickers)
- https://www.reddit.com/dev/api/ (used for links)

## Known Issues

The charts are only as good as the data available. A couple issues have been seen with data availability
- Comment data for the current day and some time periods is unavailable. Currently an educated guess is taken when these occur and the data is excluded. Remember pushshift API is not maintained directly by reddit.
- Link data can be innacurate for large time spans. The reddit API does not like returning results from years ago. More Investigation is needed.

## Future Plans

- Currently this project is just a way to aggregate and display data trends.
- I would like to expand this into the ability to discover new tickers that are trending upwards in mentions.
- Comparing with past market data it could be an interesting take on what makes market buzz.
- Can also compare different subreddits and see which ones catch on faster.

### Planned Changes

- I think there is a lot more to what makes a comment or link special than just the number of upvotes it gets. Looking into generating a *hype* score based on multiple factors including score, number of replies, upvote-downvote ration... could be interesting.
- All links and comments may also be needed to be weighted differently.
