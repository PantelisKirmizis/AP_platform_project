
import dash_bootstrap_components as dbc
from dash import dcc, html

# Builds the html layout of the Dash app
def generate_news_component(headlines):
    news_items = []
    for news in headlines:
        news_items.append(
            dbc.Card(
                dbc.CardBody([
                    html.H5(news['title'], className="card-text"),
                ]), style={'margin': 10, 'border-radius': '10px'}
            )
        )

    return news_items

def build_html_layout(fig_1, fig_2, table_1, fig_3_1, fig_3_2, fig_4_1, fig_4_2, \
            fig_5_1, fig_5_2, fig_6_1, fig_6_2, fig_7, headlines, max_value_ticker):
    
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Button('Export Report to PDF', id='export-button', className='btn btn-info')),
                    ],
                    style={'margin-bottom': 10}
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id='graph-1', figure = fig_1, style={'height': '420px'}), width=6,
                                style={'border-radius': '10px'}),
                        dbc.Col(dcc.Graph(id='graph-2', figure = fig_2, style={'height': '420px'}), width=6,
                                style={'border-radius': '10px'})
                    ],
                    style={'margin-bottom': 30}
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Img(id='table-1', src = table_1, style={'width': '100%', 'height': '250px'}),
                                width=8, style={'border-radius': '10px'}
                        )
                    ],
                    justify='center', style={'margin-bottom': 30}
                ),
                dbc.Row(
                    [
                       dbc.Col(html.Button('Initial/Current', id='toggle-button', className='btn btn-warning'), width=1),
                       dbc.Col(html.Button('Initial/Current', id='toggle-button-2', className='btn btn-warning'), width={"size": 1, "offset": 5}),
                    ],
                    style={'margin-bottom': 10}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(id='graph-3-2', src = fig_3_2, style={'display': 'block', 'width': '100%', 'height': 'auto'}),
                                html.Img(id='graph-3-1', src = fig_3_1, style={'display': 'none', 'width': '100%', 'height': 'auto'})
                            ], width=6, style={'border-radius': '10px'}
                        ),
                       dbc.Col(
                            [
                                html.Img(id='graph-4-2', src = fig_4_2, style={'display': 'block', 'width': '100%', 'height': 'auto'}),
                                html.Img(id='graph-4-1', src = fig_4_1, style={'display': 'none', 'width': '100%', 'height': 'auto'})
                            ], width=6, style={'border-radius': '10px'}
                        ),
                    ],
                    style={'margin-bottom': 30}
                ),
                dbc.Row(
                    [
                       dbc.Col(html.Button('Initial/Current', id='toggle-button-3', className='btn btn-warning'), width=1),
                       dbc.Col(html.Button('Initial/Current', id='toggle-button-4', className='btn btn-warning'), width={"size": 1, "offset": 5}),
                    ],
                    style={'margin-bottom': 10}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(id='graph-5-2', src = fig_5_2, style={'display': 'block', 'width': '100%', 'height': 'auto'}),
                                html.Img(id='graph-5-1', src = fig_5_1, style={'display': 'none', 'width': '100%', 'height': 'auto'})
                            ], width=6, style={'border-radius': '10px'}
                        ),
                       dbc.Col(
                            [
                                html.Img(id='graph-6-2', src = fig_6_2, style={'display': 'block', 'width': '100%', 'height': 'auto'}),
                                html.Img(id='graph-6-1', src = fig_6_1, style={'display': 'none', 'width': '100%', 'height': 'auto'})
                            ], width=6, style={'border-radius': '10px'}
                        ),
                    ],
                    style={'margin-bottom': 30}
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Img(id='graph-7', src = fig_7, style={'width': '100%', 'height': 'auto'}),
                                width=6, style={'border-radius': '10px'}
                        )
                    ],
                    justify='center', style={'margin-bottom': 30}
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div([
                            html.H3("Latest News related to " + max_value_ticker),
                            html.Div(id='news-container-left', children=generate_news_component(headlines[:len(headlines)//2]))
                        ]),
                            width=6
                        ),
                        dbc.Col(html.Div([html.Div(style={"margin-top": "2.8em"}),
                                html.Div(id='news-container-right', children=generate_news_component(headlines[len(headlines)//2:]))
                        ]),
                            width=6
                        )
                    ]
                ),
                dcc.Download(id="output-pdf")
            ],
            style={'background-color': '#f2f2f2', 'padding': 20, 'border-radius': '20px', 'margin': '50px'}
        )