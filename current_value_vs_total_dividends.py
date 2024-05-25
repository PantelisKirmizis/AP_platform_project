# Importing libraries

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
    
# CURRENT VALUE VS TOTAL DIVIDENDS BY ASSET
def current_value_vs_total_dividends(assets_and_investments, individual_current_value, dividend_values):

    # Calculates current value and dividends for each asset
    current_values = [individual_current_value[ticker] for ticker in assets_and_investments.keys()]
    dividend_payments = [dividend_values[ticker] for ticker in assets_and_investments.keys()]
    
    # Defines tickers and positions for the bars
    tickers = list(assets_and_investments.keys())
    x = np.arange(len(tickers))
    width = 0.35

    # Creates the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/3, current_values, width=0.4, label='Current Value', color='cornflowerblue')
    rects2 = ax.bar(x + width/3, dividend_payments, width=0.4, label='Dividends', color='lightgreen')

    # Adds labels, title, and legend
    plt.title('Current Value vs Total Dividends by Asset', loc='left', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(tickers)
    ax.legend()

    # Adds value labels on top of the bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('${:,.2f}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    # Rotates x labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Formats y-axis
    formatter = ticker.FuncFormatter(lambda x, _: '${:,.2f}'.format(x))
    ax.yaxis.set_major_formatter(formatter)

    # Removes axis lines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.tight_layout()
    
    return fig