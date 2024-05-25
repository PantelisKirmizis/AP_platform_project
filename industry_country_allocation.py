# Importing libraries

import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# INDUSTRY ALLOCATION BY COUNTRY
def industry_country_allocation(initial_assets_weights, assets_and_investments, current_assets_weights):        
  
    # INITIAL INDUSTRY ALLOCATION BY COUNTRY
    
    # Obtains all info for each asset
    info_data= {}
    for ticker in assets_and_investments.keys():
        ticker_object = yf.Ticker(ticker)  # Creates a Ticker object for each ticker in the assets_and_investments
        
        # Converts info() output from dictionary to dataframe
        info_change = pd.DataFrame.from_dict(ticker_object.info, orient="index")
        info_change.reset_index(inplace=True)
        info_change.columns = ["Info Category", "Information"]
    
        # Adds ticker and dataframe to main dictionary
        info_data[ticker] = info_change
    
    # Combines dictionary of dataframes into a single dataframe
    combined_info = pd.concat(info_data)
    combined_info = combined_info.reset_index()

    # Cleans up unnecessary column
    del combined_info["level_1"]
    combined_info.columns = ["Ticker", "Info Category", "Information"]
    
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
    
    # Groups by country and industry and sums the weights
    initial_grouped_data = initial_country_and_industry_pivot.groupby(["Country", "Industry"])["Weight"].sum().reset_index()

    # Sorts the DataFrame by country and then by industry
    initial_grouped_data = initial_grouped_data.sort_values(by=["Country", "Weight"], ascending=[True, True])

    # Gets unique countries and industries
    initial_unique_countries = initial_grouped_data["Country"].unique()
    initial_unique_industries = initial_grouped_data["Industry"].unique()

    # Calculates total weight for each country
    initial_country_totals = initial_grouped_data.groupby("Country")["Weight"].sum().reset_index()

    # Sorts unique countries based on total weight
    initial_unique_countries = initial_country_totals.sort_values(by="Weight", ascending=True)["Country"]
    
    # Creates a color palette for industries
    colors = plt.cm.Blues(np.linspace(0.2, 0.8, len(initial_unique_industries)))

    # Initializes a dictionary to store the bottom positions for each country
    bottom_positions = {country: 0 for country in initial_unique_countries}
    
    # Initializes lists to store the bars and their labels
    bars = []
    legend_labels = {}

    # Plots the stacked bar graph for industry allocation within each country
    fig1 = plt.figure(figsize=(10, 6))

    for country in initial_unique_countries:
        initial_country_data = initial_grouped_data[initial_grouped_data["Country"] == country]
        initial_total_weight = initial_country_allocation[initial_country_allocation["Country"] == country]["Weight"].iloc[0] * 100
    
        # Sorts industry groups by weight
        initial_country_data = initial_country_data.sort_values(by="Weight", ascending=True)
    
        for i, (industry, weight) in enumerate(zip(initial_country_data["Industry"], initial_country_data["Weight"])):
            # Plots the bar for the current country
            bar = plt.bar(country, weight * 100, bottom=bottom_positions[country], color=colors[i], width=0.5)
            bars.append(bar)
            
            # Stores legend label for the industry if not already stored
            if industry not in legend_labels:
                legend_labels[industry] = bar[0]
                
            bottom_positions[country] += weight * 100
            
        # Adds total percentage on top of the bar
        plt.text(country, initial_total_weight, f"{initial_total_weight:.2f}%", ha='center', va='bottom')

    # Sets labels and formatting
    plt.title('Initial Industry Allocation by Country', loc='left', pad=20)
    plt.gca().set_yticks(range(0, 101, 20))
    plt.gca().set_yticklabels(['{:.0f}%'.format(x) for x in range(0, 101, 20)])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.legend(legend_labels.values(), legend_labels.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # CURRENT INDUSTRY ALLOCATION BY COUNTRY
    
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
    
    # Groups by country and industry and sums the weights
    current_grouped_data = current_country_and_industry_pivot.groupby(["Country", "Industry"])["Weight"].sum().reset_index()

    # Sorts the DataFrame by country and then by industry
    current_grouped_data = current_grouped_data.sort_values(by=["Country", "Weight"], ascending=[True, True])

    # Gets unique countries and industries
    current_unique_countries = current_grouped_data["Country"].unique()
    current_unique_industries = current_grouped_data["Industry"].unique()

    # Calculates total weight for each country
    current_country_totals = current_grouped_data.groupby("Country")["Weight"].sum().reset_index()

    # Sorts unique countries based on total weight
    current_unique_countries = current_country_totals.sort_values(by="Weight", ascending=True)["Country"]
    
    # Creates a color palette for industries
    colors = plt.cm.Blues(np.linspace(0.2, 0.8, len(current_unique_industries)))

    # Initializes a dictionary to store the bottom positions for each country
    bottom_positions = {country: 0 for country in current_unique_countries}
    
    # Initializes lists to store the bars and their labels
    bars = []
    legend_labels = {}

    # Plots the stacked bar graph for industry allocation within each country
    fig2 = plt.figure(figsize=(10, 6))

    for country in current_unique_countries:
        current_country_data = current_grouped_data[current_grouped_data["Country"] == country]
        current_total_weight = current_country_allocation[current_country_allocation["Country"] == country]["Weight"].iloc[0] * 100
    
        # Sorts industry groups by weight
        current_country_data = current_country_data.sort_values(by="Weight", ascending=True)
    
        for i, (industry, weight) in enumerate(zip(current_country_data["Industry"], current_country_data["Weight"])):
            # Plots the bar for the current country
            bar = plt.bar(country, weight * 100, bottom=bottom_positions[country], color=colors[i], width=0.5)
            bars.append(bar)
            
            # Stores legend label for the industry if not already stored
            if industry not in legend_labels:
                legend_labels[industry] = bar[0]
                
            bottom_positions[country] += weight * 100
            
        # Adds total percentage on top of the bar
        plt.text(country, current_total_weight, f"{current_total_weight:.2f}%", ha='center', va='bottom')

    # Sets labels and formatting
    plt.title('Current Industry Allocation by Country', loc='left', pad=20)
    plt.gca().set_yticks(range(0, 101, 20))
    plt.gca().set_yticklabels(['{:.0f}%'.format(x) for x in range(0, 101, 20)])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.legend(legend_labels.values(), legend_labels.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    return fig1, fig2
        