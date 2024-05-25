# Importing libraries

import pandas as pd
import yfinance as yf

# OVERVIEW TABLE
def overview_table(assets_and_investments, df, dividend_values, dividend_count, 
                   initial_total_portfolio_value, date_to, date_from, 
                   individual_current_value, capital_gains, net_profit_loss, 
                   portfolio_current_value, portfolio_capital_gains, portfolio_net_gains):
    
    # Leaves the Ticker name and the value in a dataframe format
    individual_current_value_df = pd.DataFrame(list(individual_current_value.items()), columns=['Ticker', 'Current Value']) 
    individual_current_value_df.set_index('Ticker', inplace=True)
    capital_gains_df = pd.DataFrame(list(capital_gains.items()), columns=['Ticker', 'Capital Gains'])
    capital_gains_df.set_index('Ticker', inplace=True)
    net_profit_loss_df = pd.DataFrame(list(net_profit_loss.items()), columns=['Ticker', 'Net Profit/Loss'])
    net_profit_loss_df.set_index('Ticker', inplace=True)

    # Calculates portfolio's total dividend payments and total value of the dividends paid during time period
    portfolio_dividend_count = dividend_count['Dividend Payments'].sum() 
    portfolio_total_dividend_value = sum(dividend_values.values()) 
    
    # Shows the name of the asset and the value in a dataframe format
    dividend_values_df = pd.DataFrame(list(dividend_values.items()), columns=['Ticker', 'Dividends'])
    dividend_values_df.set_index('Ticker', inplace=True)
    
    # Creates an overview table
    overview_table = pd.DataFrame({
        'Current Value': individual_current_value_df['Current Value'],
        'Capital Gains': capital_gains_df['Capital Gains'],
        'Net Profit/Loss': net_profit_loss_df['Net Profit/Loss'],
        'Dividend Payments': dividend_count['Dividend Payments'],
        'Dividends': dividend_values_df['Dividends']
    }, index=net_profit_loss_df.index)

    
    # Adds a row for the portfolio
    overview_table.loc['Portfolio'] = [portfolio_current_value, portfolio_capital_gains, 
                                        portfolio_net_gains, portfolio_dividend_count, portfolio_total_dividend_value]
    
    # Sets the index name to an empty string
    overview_table.index.name = ''

    # Formats values in the table
    overview_table['Current Value'] = overview_table['Current Value'].map('${:,.2f}'.format)
    overview_table['Capital Gains'] = overview_table['Capital Gains'].map('{:,.2f}%'.format)
    overview_table['Net Profit/Loss'] = overview_table['Net Profit/Loss'].map('${:,.2f}'.format)
    overview_table['Dividend Payments'] = overview_table['Dividend Payments'].astype(int).map('{:,.0f}'.format)
    overview_table['Dividends'] = overview_table['Dividends'].map('${:,.2f}'.format)
    
    # Styles and aligns the table
    def color_positive_negative(value):
        if isinstance(value, str):  # Checks if value is already formatted
            value = float(value.replace('%', '').replace('$', '').replace(',', ''))  # Converts to float
        if value > 0:
            color = 'limegreen'
        elif value < 0:
            color = 'red'
        else:
            color = 'black'
        return 'color: %s' % color
    
    # Styles and aligns the table
    overview_table_formatted = overview_table.style \
    .set_properties(**{'text-align': 'center'}) \
    .applymap(color_positive_negative, subset=['Capital Gains', 'Net Profit/Loss'])
    
    # Defines custom CSS to adjust the position of the column names
    custom_css = [
        {
            'selector': 'thead th',  # Selects the header cells
            'props': [('position', 'relative'), ('top', '30px')]  # Moves the header cells 20px upwards
        }
    ]
    
    # Applies custom CSS
    overview_table_formatted.set_table_styles(custom_css)

    # Returns the styled table
    return overview_table_formatted