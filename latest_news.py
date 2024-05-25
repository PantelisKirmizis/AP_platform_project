# Importing libraries

import yfinance as yf

# MOST CURRENT NEWS FOR THE ASSET WITH THE HIGHEST CURRENT VALUE
def latest_news(individual_current_value):
     
    # Finds the asset with the biggest current value
    max_value_ticker = max(individual_current_value, key=individual_current_value.get)

    # Creates a Ticker object for the asset
    asset_ticker = yf.Ticker(max_value_ticker)

    # Gets the latest news headlines
    news_headlines = asset_ticker.news
    
    return news_headlines, max_value_ticker
