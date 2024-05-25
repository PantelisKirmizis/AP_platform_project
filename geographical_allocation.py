# Importing libraries

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# GEOGRAPHICAL ALLOCATION
def geographical_allocation(initial_assets_weights, assets_and_investments, current_assets_weights):
 
    # INITIAL GEOGRAPHICAL ALLOCATION        
        
    # Obtains all info for each asset
    info_data= {}
    for ticker in assets_and_investments.keys():  # Initiates a loop that iterates through each ticker in the assets_and_investments
        ticker_object = yf.Ticker(ticker)
        
        # Converts info() output from dictionary to dataframe
        info_change = pd.DataFrame.from_dict(ticker_object.info, orient="index")
        info_change.reset_index(inplace=True)
        info_change.columns = ["Info Category", "Information"]
    
        # Adds ticker and dataframe to main dictionary
        info_data[ticker] = info_change
    
    # Combines dictionary of dataframes into a single dataframe
    combined_info = pd.concat(info_data)
    combined_info = combined_info.reset_index()

    # Cleans up unnecessary column and updates column names
    del combined_info["level_1"]
    combined_info.columns = ["Ticker", "Info Category", "Information"]
    
    country = combined_info[combined_info["Info Category"]=="country"].reset_index()

    # Filters the combined_info DataFrame for rows with "country" or "industry" in the "Info Category" column
    initial_country_and_industry = combined_info[combined_info["Info Category"].isin(["country", "industry"])]

    # Pivots the DataFrame to have tickers as rows and countries and industries as columns
    initial_country_and_industry_pivot = initial_country_and_industry.pivot(index="Ticker", columns="Info Category", values="Information").reset_index()

    # Renames the columns for clarity
    initial_country_and_industry_pivot.columns.name = None
    initial_country_and_industry_pivot.columns = ["Ticker", "Country", "Industry"]
    initial_country_and_industry_pivot["Weight"] = initial_country_and_industry_pivot["Ticker"].map(initial_assets_weights)
    
    # Groups by country and calculates the total allocation percentage for each country
    initial_industry_allocation = initial_country_and_industry_pivot.groupby("Industry")["Weight"].sum().reset_index()

    # Sorts the DataFrame by allocation percentage in descending order
    initial_industry_allocation = initial_industry_allocation.sort_values(by="Weight")    
    
    # Groups by country and calculates the total allocation percentage for each country
    initial_country_allocation = initial_country_and_industry_pivot.groupby("Country")["Weight"].sum().reset_index()
   
    # Sorts the DataFrame by allocation percentage in descending order
    initial_country_allocation = initial_country_allocation.sort_values(by="Weight")    

    # Plots the bar graph
    fig1 = plt.figure(figsize=(10, 6))
    bars1 = plt.bar(initial_country_allocation["Country"], initial_country_allocation["Weight"] * 100, color='cornflowerblue', width=0.4)
    plt.title('Initial Geographical Allocation', loc='left', pad=20)
    
    # Sets y-axis ticks and labels
    plt.gca().set_yticks(range(0, 101, 20))
    plt.gca().set_yticklabels(['{:.0f}%'.format(x) for x in range(0, 101, 20)])

    # Removes axis lines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    # Adds percentage labels on top of each bar
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, '{:.2f}%'.format(yval), va='bottom', ha='center')

    # CURRENT GEOGRAPHICAL ALLOCATION     
    
    # Filters the combined_info DataFrame for rows with "country" or "industry" in the "Info Category" column
    current_country_and_industry = combined_info[combined_info["Info Category"].isin(["country", "industry"])]

    # Pivots the DataFrame to have tickers as rows and countries and industries as columns
    current_country_and_industry_pivot = current_country_and_industry.pivot(index="Ticker", columns="Info Category", values="Information").reset_index()

    # Renames the columns for clarity
    current_country_and_industry_pivot.columns.name = None
    current_country_and_industry_pivot.columns = ["Ticker", "Country", "Industry"]
    current_country_and_industry_pivot["Weight"] = current_country_and_industry_pivot["Ticker"].map(current_assets_weights)

    # Groups by country and calculates the total allocation percentage for each country
    current_industry_allocation = current_country_and_industry_pivot.groupby("Industry")["Weight"].sum().reset_index()

    # Sorts the DataFrame by allocation percentage in descending order
    current_industry_allocation = current_industry_allocation.sort_values(by="Weight")
    
    # Groups by country and calculates the total allocation percentage for each country
    current_country_allocation = current_country_and_industry_pivot.groupby("Country")["Weight"].sum().reset_index()
   
    # Sorts the DataFrame by allocation percentage in descending order
    current_country_allocation = current_country_allocation.sort_values(by="Weight")

    # Plots the bar graph
    fig2 = plt.figure(figsize=(10, 6))
    bars2 = plt.bar(current_country_allocation["Country"], current_country_allocation["Weight"] * 100, color='cornflowerblue', width=0.4)
    plt.title('Current Geographical Allocation', loc='left', pad=20)
    
    # Sets y-axis ticks and labels
    plt.gca().set_yticks(range(0, 101, 20))
    plt.gca().set_yticklabels(['{:.0f}%'.format(x) for x in range(0, 101, 20)])

    # Removes axis lines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    # Adds percentage labels on top of each bar
    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, '{:.2f}%'.format(yval), va='bottom', ha='center') 

    return fig1, fig2
        