
# Import modules
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import yfinance as yf
from datetime import datetime
from fpdf import FPDF

from individual_asset_performance import individual_asset_performance
from portfolio_performance_vs_benchmark import portfolio_performance_vs_benchmark
from overview_table import overview_table
from portfolio_allocation import portfolio_allocation
from geographical_allocation import geographical_allocation
from industry_allocation import industry_allocation
from industry_country_allocation import industry_country_allocation
from current_value_vs_total_dividends import current_value_vs_total_dividends
from latest_news import latest_news
from build_html_layout import build_html_layout

from utils import string_to_dict
from utils import matplotlib_fig_to_img
from utils import dataframe_table_to_img
from utils import toggle_images
from utils import build_pdf

# Starts the Dash app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Defines the layout of the page
app.layout = html.Div(
    [
     
        # Headers of dashboard
        html.H1('Stock Portfolio Tracker', style={'text-align': 'center', 'padding-top': 50}),
        html.H2('An interactive dashboard', style={'text-align': 'center'}),

        html.Div(
            html.P("Enter your desired stock tickers (exactly as they appear on Yahoo Finance) and the total amount "
                   "invested for each security in your portfolio in a dictionary format (Ticker1: Value1, Ticker2: "
                   "Value2...). Select a benchmark ticker and a date range (dd/mm/yyyy). Select dates when the market was open. "
                   "Then click Submit to show results. ",
               style={'text-align': 'center'}
               ),
            style={'max-width': '800px', 'margin': '0 auto', 'padding-top': 20}
        ),

        # Input divs
        html.Div(
            [
                dbc.Input(id='ticker-input', placeholder='Enter tickers here (dictionary format)...', style={'width': '60%'}),
                dbc.Input(id='benchmark-input', placeholder='Enter benchmark ticker here...', className='ms-3', style={'width': '20%'}),
            ],
            style={'display': 'flex', 'justify-content': 'center'},
            className='mt-5 mb-3'
        ),
        
        html.Div(
            [
                dcc.DatePickerRange(id='date-range-input', display_format='DD/MM/YYYY'),
                html.Button('Submit', id='submit-val', n_clicks=0, className='ms-3 btn btn-primary')
            ],
            style={'display': 'flex', 'justify-content': 'center'},
            className='mb-3'
        ),
        
        # Divider
        html.Hr(style={'margin-top': 30}),
        
        # Here the output div will be rendered after submit is pressed
        html.Div(id='output-div')
    ],
    style={'padding-bottom': 100}
)

@app.callback(
    Output('output-div', 'children'),
    Input(component_id = 'submit-val', component_property = 'n_clicks'),
    State(component_id = 'ticker-input', component_property = 'value'),
    State(component_id = 'benchmark-input', component_property = 'value'),
    [State('date-range-input', 'start_date'), State('date-range-input', 'end_date')]
)
def update_graphs(n_clicks, assets_and_investments, benchmark, start_date, end_date):
    
    # Do not update anything before Submit button is pressed
    if n_clicks == 0:
        raise PreventUpdate
    
    # Converts text input to dictionary
    assets_and_investments = string_to_dict(assets_and_investments)
    
    # If no ticker or benchmark was given, do not do anything!
    if len(assets_and_investments) == 0 or \
        not benchmark or \
        not start_date or \
        not end_date:
        return html.Div(html.H4("Make sure to enter all required inputs above!", style={'margin-top': 20,
                                                                                        'text-align': 'center', 'color': 'red'}))
    
    # Converts date range to proper format
    date_from = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    date_to = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    
    # Obtains assets' data with yfinance
    df = yf.download(tickers=list(assets_and_investments.keys()),
                     start=date_from, end=date_to)

    # If one or all tickers given start after start date given, do not do anything!
    if len(df) == 0:
        return html.Div(html.H4("Data unavailable for one or all selected tickers for the given date range!", style={'margin-top': 20,
                                'text-align': 'center', 'color': 'red'}))

    if len(assets_and_investments.keys()) == 1:
        first_valid_index = df['Adj Close'].to_frame().first_valid_index()
        if first_valid_index and first_valid_index.strftime('%Y-%m-%d') > start_date:
            return html.Div(html.H4("Data unavailable for one or all selected tickers for the given date range!", style={'margin-top': 20,
                                    'text-align': 'center', 'color': 'red'}))

    if len(assets_and_investments.keys()) > 1:
        for ticker in assets_and_investments.keys():
            first_valid_index = df['Adj Close'][ticker].first_valid_index()
            if first_valid_index.strftime('%Y-%m-%d') > start_date:
                return html.Div(html.H4("Data unavailable for one or all selected tickers for the given date range!", style={'margin-top': 20,
                                        'text-align': 'center', 'color': 'red'}))

# CALCULATION OF SOME COMMON VALUES ACROSS MULTIPLE FUNCTIONS
    
    # Calculates portfolio value
    initial_total_portfolio_value = sum(assets_and_investments.values())
    
    # Calculates the weights of the portfolio
    initial_assets_weights = {ticker: value / initial_total_portfolio_value for ticker, value in assets_and_investments.items()} #a dictionary comprehension that iterates over each key-value pair in assets_and_prices.items(). For each pair, it calculates the weight of the asset by dividing its value by the total portfolio value, and then assigns this weight to the asset name (assets) in the resulting dictionary.
    
    # Checks if dataframe has MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df = df['Adj Close'].fillna(df['Close'])  # If 'Adjusted Close' is not available, uses 'Close'
        
    # Checks if there are more than just one security in the portfolio
    if len(initial_assets_weights) > 1:
        initial_weights = list(initial_assets_weights.values())
        weighted_returns = df.pct_change().mul(initial_weights, axis = 1)  # Computes weighted returns
        portfolio_returns = weighted_returns.sum(axis=1)  # Sums weighted returns to build portfolio returns
    # If there is only one security in the portfolio...
    else:
        df = df['Adj Close'].fillna(df['Close'])  # If 'Adjusted Close' is not available, uses 'Close'
        portfolio_returns = df.pct_change()  # Computes returns without weights
    
    # If working with only one ticker, make sure df has the right format
    if isinstance(df, pd.Series):
        df = df.to_frame()
        df.columns = list(assets_and_investments.keys())
    
    # Obtains benchmark data with yfinance
    benchmark_df = yf.download(benchmark, 
                               start=date_from, end=date_to) 
    # If 'Adjusted Close' is not available, uses 'Close'
    benchmark_df = benchmark_df['Adj Close'].fillna(benchmark_df['Close'])
    
    # Computes benchmark returns
    benchmark_returns = benchmark_df.pct_change()
    
    # Obtains dividend data for each asset
    dividend_data = {}
    for ticker in assets_and_investments.keys():
        dividend_data[ticker] = yf.Ticker(ticker).dividends
    
    # Concatenates dividend data into a DataFrame
    dividend_df = pd.concat(dividend_data, axis=1)
    dividend_df.columns = assets_and_investments.keys()
    
    # Calculates the number of times each asset paid dividends during the selected period
    dividend_count = pd.DataFrame(index=dividend_df.columns)
    for ticker in dividend_df.columns:
        # Filters dividends within the specified period and counts the occurrences
        dividend_count.loc[ticker, 'Dividend Payments'] = dividend_df[ticker][(dividend_df.index >= date_from) & (dividend_df.index <= date_to)].count() 

    # Fills missing values (if no dividends were paid during the period) with 0
    dividend_count.fillna(0, inplace=True)

    # Calculates the total value generated by all dividend payments for each asset
    dividend_values = {}
    for ticker in assets_and_investments.keys():
        # Finds the number of shares bought for each asset
        shares_bought = assets_and_investments[ticker] / df.iloc[0][ticker]
        # Multiplies the number of stocks with the dividends data from yf and sums all the results within the given period
        dividend_values[ticker] = (dividend_df[ticker][(dividend_df.index >= date_from) & (dividend_df.index <= date_to)] * shares_bought).sum() # It shows the name of the asset and the value
    
    # Calculates the total value for each asset for the current date
    individual_current_value = {}
    net_profit_loss = {}
    capital_gains = {}
    for ticker in assets_and_investments.keys():
        # Finds the number of shares bought for each asset
        shares_bought = assets_and_investments[ticker] / df.iloc[0][ticker]
        # Gets the last Adj Close price available
        last_price = df.iloc[-1][ticker]
        # Calculates the current value of each asset and stores it in dictionary
        individual_current_value[ticker] = shares_bought * last_price
        # Calculates the net profit of each asset and stores it in dictionary
        net_profit_loss[ticker] = individual_current_value[ticker] - assets_and_investments[ticker]
        # Calculates the capital gain of each asset and stores it in dictionary
        capital_gains[ticker] = (net_profit_loss[ticker] / assets_and_investments[ticker]) * 100
    
    # Calculates portfolio's most current value, net gains, and capital gains
    portfolio_current_value = sum(individual_current_value.values())
    portfolio_net_gains = portfolio_current_value - initial_total_portfolio_value
    portfolio_capital_gains = (portfolio_net_gains / initial_total_portfolio_value) * 100
    
    # Calculates current assets weights
    current_assets_weights = {}
    for ticker in assets_and_investments.keys():
        current_assets_weights[ticker] = (individual_current_value[ticker] / portfolio_current_value)
    
# CREATION OF FIGURES TO RETURN
    
    # Creates figures and tables
    fig_1 = individual_asset_performance(initial_assets_weights, df)
    fig_2 = portfolio_performance_vs_benchmark(portfolio_returns, benchmark_returns)
    table_1 = overview_table(assets_and_investments, df, dividend_values, dividend_count, initial_total_portfolio_value, 
                    date_to, date_from, individual_current_value, capital_gains, 
                    net_profit_loss, portfolio_current_value, portfolio_capital_gains, portfolio_net_gains)
    fig_3_1, fig_3_2 = portfolio_allocation(initial_assets_weights, assets_and_investments, individual_current_value, portfolio_current_value, current_assets_weights)
    fig_4_1, fig_4_2 = geographical_allocation(initial_assets_weights, assets_and_investments, current_assets_weights)
    fig_5_1, fig_5_2 = industry_allocation(initial_assets_weights, assets_and_investments, current_assets_weights)
    fig_6_1, fig_6_2 = industry_country_allocation(initial_assets_weights, assets_and_investments, current_assets_weights)
    fig_7 = current_value_vs_total_dividends(assets_and_investments, individual_current_value, dividend_values)
    headlines, max_value_ticker = latest_news(individual_current_value)
    
    # Stores figures in app's context
    app.ctx = {'fig_1': fig_1,
                'fig_2': fig_2,
                'table_1': dataframe_table_to_img(table_1),
                'fig_3_1': matplotlib_fig_to_img(fig_3_1),
                'fig_3_2': matplotlib_fig_to_img(fig_3_2),
                'fig_4_1': matplotlib_fig_to_img(fig_4_1),
                'fig_4_2': matplotlib_fig_to_img(fig_4_2),
                'fig_5_1': matplotlib_fig_to_img(fig_5_1),
                'fig_5_2': matplotlib_fig_to_img(fig_5_2),
                'fig_6_1': matplotlib_fig_to_img(fig_6_1),
                'fig_6_2': matplotlib_fig_to_img(fig_6_2),
                'fig_7': matplotlib_fig_to_img(fig_7),
                'headlines': headlines,
                'start_date': date_from,
                'end_date': date_to
                }
    
    return build_html_layout(fig_1, fig_2, dataframe_table_to_img(table_1),
            matplotlib_fig_to_img(fig_3_1), matplotlib_fig_to_img(fig_3_2),
            matplotlib_fig_to_img(fig_4_1), matplotlib_fig_to_img(fig_4_2),
            matplotlib_fig_to_img(fig_5_1), matplotlib_fig_to_img(fig_5_2),
            matplotlib_fig_to_img(fig_6_1), matplotlib_fig_to_img(fig_6_2),
            matplotlib_fig_to_img(fig_7),
            headlines, max_value_ticker)
                

@app.callback(
    Output(component_id='graph-3-1', component_property='style'),
    Output(component_id='graph-3-2', component_property='style'),
    Input(component_id='toggle-button', component_property='n_clicks'),
    State(component_id='graph-3-1', component_property='style'),
    State(component_id='graph-3-2', component_property='style')
)
def toggle_images_1(n_clicks, img1_style, img2_style):
    return toggle_images(n_clicks, img1_style, img2_style)
                      
@app.callback(
    Output(component_id='graph-4-1', component_property='style'),
    Output(component_id='graph-4-2', component_property='style'),
    Input(component_id='toggle-button-2', component_property='n_clicks'),
    State(component_id='graph-4-1', component_property='style'),
    State(component_id='graph-4-2', component_property='style')
)
def toggle_images_2(n_clicks, img1_style, img2_style):
    return toggle_images(n_clicks, img1_style, img2_style)
                      
@app.callback(
    Output(component_id='graph-5-1', component_property='style'),
    Output(component_id='graph-5-2', component_property='style'),
    Input(component_id='toggle-button-3', component_property='n_clicks'),
    State(component_id='graph-5-1', component_property='style'),
    State(component_id='graph-5-2', component_property='style')
)
def toggle_images_3(n_clicks, img1_style, img2_style):
    return toggle_images(n_clicks, img1_style, img2_style)
                      
@app.callback(
    Output(component_id='graph-6-1', component_property='style'),
    Output(component_id='graph-6-2', component_property='style'),
    Input(component_id='toggle-button-4', component_property='n_clicks'),
    State(component_id='graph-6-1', component_property='style'),
    State(component_id='graph-6-2', component_property='style')
)
def toggle_images_4(n_clicks, img1_style, img2_style):
    return toggle_images(n_clicks, img1_style, img2_style)
                  
@app.callback(
    Output(component_id='output-pdf', component_property='data'),
    Input(component_id='export-button', component_property='n_clicks'),
    prevent_initial_call=True
)
def export_pdf(n_clicks):
    
    if not hasattr(app, 'ctx') or len(app.ctx) == 0:
        return None
    
    def create_pdf(bytes_io):
        
        pdf = FPDF(orientation='L')
        
        build_pdf(pdf, app.ctx)
    
        pdf_data = pdf.output(dest = 'S').encode('latin-1')
        bytes_io.write(pdf_data)
    
    return dcc.send_bytes(create_pdf, 'output.pdf')

if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)
