# Importing libraries

import pandas as pd
import plotly.graph_objs as go
    
# INDIVIDUAL ASSET PERFORMANCE
def individual_asset_performance(initial_assets_weights, df):

    # Starts DataFrame and Series
    individual_cumsum = pd.DataFrame()
    
    # Iterates through tickers and weights in the tickers_weights dictionary
    for ticker, weight in initial_assets_weights.items():
        if ticker in df.columns:  # Confirms that the tickers are available
            individual_returns = df[ticker].pct_change()  # Computes individual daily returns for each ticker
            individual_cumsum[ticker] = ((1 + individual_returns).cumprod() - 1)   # Computes cumulative returns over the period for each ticker
            
    fig_individual = go.Figure(
        layout = go.Layout(
            title=go.layout.Title(text = "Individual Asset Performance")
            )
        )
            
    # Adds cumulative returns of each individual asset to the plot
    for ticker in individual_cumsum.columns:
         fig_individual.add_trace(go.Scatter(x=individual_cumsum.index,
                                  y=individual_cumsum[ticker],
                                  mode = 'lines',
                                  name = ticker))
        
    # Adjusts the layout to make the graph larger vertically and changes the title of the legend
    fig_individual.update_layout(height=420,legend_title="Assets",template = 'plotly_white',hovermode='x unified')

    # Adds the historical returns for each ticker on the plot    
    fig_individual.update_yaxes(title_text='Cumulative Returns',
                                tickformat =',.2%',
                                showspikes=True,spikesnap="cursor",spikemode="across")
    fig_individual.update_xaxes(showspikes=True,spikesnap="cursor",
        rangeslider_visible=True,
        # Creates buttons for 1 month, 3 months, 6 months, 1 year, Year to Date, and all dates
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    
    return fig_individual