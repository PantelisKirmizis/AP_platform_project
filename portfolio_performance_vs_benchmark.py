# Importing libraries

import plotly.express as px
import plotly.graph_objs as go
    
# PORTFOLIO PERFORMANCE VS BENCHMARK
def portfolio_performance_vs_benchmark(portfolio_returns, benchmark_returns):
    
    # Computes the cumulative returns for the portfolio and the benchmark
    portfolio_cumsum = ((1 + portfolio_returns).cumprod() - 1) 
    benchmark_cumsum = ((1 + benchmark_returns).cumprod() - 1) 
    
    fig_portfolio_benchmark = px.line(title='Portfolio Performance vs Benchmark')
    
    # Adds the cumulative returns for the portfolio
    fig_portfolio_benchmark.add_trace(go.Scatter(x=portfolio_cumsum.index, 
                              y = portfolio_cumsum,
                              mode = 'lines', name = 'Portfolio'))
    
    # Adds the cumulative returns for the benchmark
    fig_portfolio_benchmark.add_trace(go.Scatter(x=benchmark_cumsum.index, 
                              y = benchmark_cumsum,
                              mode = 'lines', name = 'Benchmark'))
    
    # Adjusts the layout to make the graph larger vertically and changes the title of the legend
    fig_portfolio_benchmark.update_layout(height=420,template = 'plotly_white',hovermode='x unified')

    # Adds the historical returns for each ticker on the plot    
    fig_portfolio_benchmark.update_yaxes(title_text='Cumulative Returns',
                                tickformat =',.2%',
                                showspikes=True,spikesnap="cursor",spikemode="across")
    fig_portfolio_benchmark.update_xaxes(showspikes=True,spikesnap="cursor",
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
    
    return fig_portfolio_benchmark