# Importing libraries

import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# INDUSTRY ALLOCATION
def industry_allocation(initial_assets_weights, assets_and_investments, current_assets_weights):
            
    # INITIAL INDUSTRY ALLOCATION             
        
    # Defines the number of colors in the palette
    number_colors = len(initial_assets_weights)
    
    # Generates a palette of blue colors
    blue_palette = cm.Blues(np.linspace(0.2, 0.8, number_colors))
    
    # Obtains all info for each asset
    info_data= {}
    for ticker in assets_and_investments.keys():
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
    
    # Sets the size of the pie chart
    fig1, ax1 = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"))

    # Obtains tickers and weights
    labels=list(initial_industry_allocation["Industry"])  
    values=list(initial_industry_allocation["Weight"]) 

    # Plots the pie chart
    wedges, texts = ax1.pie(values, wedgeprops=dict(width=0.5), startangle=-40, colors=blue_palette)

    # Sets the arrows connecting the labels to the pie chart
    kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=None, zorder=0, va="center")

    # Iterates over the wedges of the pie chart and their corresponding index i.
    for i, p in enumerate(wedges): 
        ang = (p.theta2 - p.theta1)/2. + p.theta1  # Calculates the angle at midpoint of each wedge.
        y = np.sin(np.deg2rad(ang))  # Calculates the coordinates of the label position based on the angle
        x = np.cos(np.deg2rad(ang)) 
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax1.annotate(f'{labels[i]} {values[i]*100:.2f}%', xy=(x, y), xytext=(1.1*np.sign(x), 1.1*y),
                    horizontalalignment=horizontalalignment, **kw)

    ax1.set_title("Initial Industry Allocation", loc='left', pad=20)
  
    # CURRENT INDUSTRY ALLOCATION
    
    # Filters the combined_info DataFrame for rows with "country" or "industry" in the "Info Category" column
    current_country_and_industry = combined_info[combined_info["Info Category"].isin(["country", "industry"])]

    # Pivots the DataFrame to have tickers as rows and countries and industries as columns
    current_country_and_industry_pivot = current_country_and_industry.pivot(index="Ticker", columns="Info Category", values="Information").reset_index()

    # Rename the columns for clarity
    current_country_and_industry_pivot.columns.name = None  # Remove the column index name
    current_country_and_industry_pivot.columns = ["Ticker", "Country", "Industry"]
    current_country_and_industry_pivot["Weight"] = current_country_and_industry_pivot["Ticker"].map(current_assets_weights)

    # Grouping by country and calculating the total allocation percentage for each country
    current_industry_allocation = current_country_and_industry_pivot.groupby("Industry")["Weight"].sum().reset_index()

    # Sorting the DataFrame by allocation percentage in descending order
    current_industry_allocation = current_industry_allocation.sort_values(by="Weight")
    
      # Grouping by country and calculating the total allocation percentage for each country
    current_country_allocation = current_country_and_industry_pivot.groupby("Country")["Weight"].sum().reset_index()
   
    # Sorting the DataFrame by allocation percentage in descending order
    current_country_allocation = current_country_allocation.sort_values(by="Weight")
    
    # Sets the size of the pie chart
    fig2, ax2 = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"))

    # Obtains tickers and weights
    labels=list(current_industry_allocation["Industry"])  
    values=list(current_industry_allocation["Weight"]) 

    # Plots the pie chart
    wedges, texts = ax2.pie(values, wedgeprops=dict(width=0.5), startangle=-40, colors=blue_palette)

    # Sets the arrows connecting the labels to the pie chart
    kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=None, zorder=0, va="center")

    # Iterates over the wedges of the pie chart and their corresponding index i.
    for i, p in enumerate(wedges): 
        ang = (p.theta2 - p.theta1)/2. + p.theta1  # Calculates the angle at midpoint of each wedge.
        y = np.sin(np.deg2rad(ang))  # Calculates the coordinates of the label position based on the angle
        x = np.cos(np.deg2rad(ang)) 
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax2.annotate(f'{labels[i]} {values[i]*100:.2f}%', xy=(x, y), xytext=(1.1*np.sign(x), 1.1*y),
                    horizontalalignment=horizontalalignment, **kw)

    ax2.set_title("Current Industry Allocation", loc='left', pad=20)   

    return fig1, fig2
        