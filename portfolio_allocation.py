# Importing libraries

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# PORTFOLIO ALLOCATION
def portfolio_allocation(initial_assets_weights, assets_and_investments, individual_current_value, portfolio_current_value, current_assets_weights):

    # INITIAL PORTFOLIO ALLOCATION
    
    # Defines the number of colors in the palette
    number_colors = len(initial_assets_weights)

    # Generates a palette of blue colors
    blue_palette = cm.Blues(np.linspace(0.2, 0.8, number_colors))
    
    # Sets the size of the pie chart
    fig1, ax1 = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"))

    # Obtains tickers and weights
    labels=list(initial_assets_weights.keys())  
    values=list(initial_assets_weights.values()) 

    # Plots the pie chart
    wedges, texts = ax1.pie(values, wedgeprops=dict(width=0.5), startangle=-40, colors=blue_palette)

    # Sets the arrows connecting the labels to the pie chart
    kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=None, zorder=0, va="center")

    # Iterates over the wedges of the pie chart and their corresponding index i.
    for i, p in enumerate(wedges): 
        ang = (p.theta2 - p.theta1)/2. + p.theta1 # Calculates the angle at midpoint of each wedge. 
        y = np.sin(np.deg2rad(ang)) # Calculates the coordinates of the label position based on the angle.
        x = np.cos(np.deg2rad(ang)) 
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}" # Defines the connection style for the annotation arrow
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax1.annotate(f'{labels[i]} {values[i]*100:.2f}%', xy=(x, y), xytext=(1.1*np.sign(x), 1.1*y),
                    horizontalalignment=horizontalalignment, **kw)

    ax1.set_title("Initial Portfolio Allocation", loc='left', pad=20)
        
    # CURRENT PORTFOLIO ALLOCATION    
        
    # Sets the size of the pie chart
    fig2, ax2 = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"))

    # Obtains tickers and weights
    labels=list(current_assets_weights.keys())  
    values=list(current_assets_weights.values()) 

    # Plots the pie chart
    wedges, texts = ax2.pie(values, wedgeprops=dict(width=0.5), startangle=-40, colors=blue_palette)

    # Sets the arrows connecting the labels to the pie chart
    kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=None, zorder=0, va="center")

    # Iterates over the wedges of the pie chart and their corresponding index i.
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1 # Calculates the angle at midpoint of each wedge. 
        y = np.sin(np.deg2rad(ang)) # Calculates the coordinates of the label position based on the angle 
        x = np.cos(np.deg2rad(ang)) 
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}" # Defines the connection style for the annotation arrow
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax2.annotate(f'{labels[i]} {values[i]*100:.2f}%', xy=(x, y), xytext=(1.1*np.sign(x), 1.1*y),
                    horizontalalignment=horizontalalignment, **kw)

    ax2.set_title("Current Portfolio Allocation", loc='left', pad=20)

    return fig1, fig2
        