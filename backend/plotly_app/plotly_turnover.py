import plotly.graph_objs as go
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

from django_plotly_dash import DjangoDash
from ordercast_order.repositories import OrderRepository
from plotly_app.style import input_style

# Create a DjangoDash app
app = DjangoDash('TurnoverApp')


def calculate_turnover():
    """ Calculates the turnover value """

    # Turnover per client Diagram
    client_diagram_data = OrderRepository.client_diagram_data()

    # Turnover per client Table
    client_turnover_data = OrderRepository.client_turnover_data()

    # Turnover per Country
    country_turnover_data = OrderRepository.country_turnover_data()

    return client_diagram_data, client_turnover_data, country_turnover_data


# Layout of the app
app.layout = html.Div([

    html.H1('Turnover Analysis'),

    dcc.Dropdown(
        id='data-type-dropdown',
        options=[
            {'label': 'Client', 'value': 'client'},
            {'label': 'Country', 'value': 'country'}
        ],
        value='client',
        clearable=False,
        style={'width': '50%'}
    ),

    dcc.Graph(id='turnover-graph'),

    html.Br(),
    html.H2("Turnover per merchant"),
    html.Br(),

    html.Div(children=[
        dcc.Input(
            id="search_clients",
            type="text",
            placeholder="Search by merchant name or email",
            style=input_style
        ),
    ], style={'display': 'flex', 'flexDirection': 'row'}),

    html.Div(children=[
        html.Div(
            [
                html.Br(),
                dash_table.DataTable(
                    id="client-table",
                    columns=[
                        {"name": "Client", "id": "client__username"},
                        {"name": "Email", "id": "client__email"},
                        {"name": "Total Turnover", "id": "turnover"},
                    ],
                    page_size=10,
                    sort_action="native",
                    style_cell=dict(textAlign='center'),
                ),
            ],
        ),
    ]),

    html.Br(),
    html.H2("Turnover per country"),
    html.Br(),

    html.Div(children=[
        dcc.Input(
            id="search_country",
            type="text",
            placeholder="Search by country",
            style=input_style
        ),
    ], style={'display': 'flex', 'flexDirection': 'row'}),

    html.Div(children=[
        html.Div(
            [
                html.Br(),
                dash_table.DataTable(
                    id="country-table",
                    columns=[
                        {"name": "Country", "id": "billing_country__name"},
                        {"name": "Total Turnover", "id": "turnover"}
                    ],
                    page_size=10,
                    sort_action="native",
                    style_cell=dict(textAlign='center'),
                ),
            ],
        ),
    ]),
])


@app.callback(
    Output('turnover-graph', 'figure'),
    [Input('data-type-dropdown', 'value')]
)
def update_graph(selected_data_type):
    """ Update the graph """

    # Calculate total price data
    client_diagram_data, _, country_turnover_data = calculate_turnover()

    # Prepare data for the graph depending on the selected data type
    if selected_data_type == 'client':
        labels = [f"{client['client__tariff_name']} - ${client['total_price']}" for client in client_diagram_data]
        values = [client['total_price'] for client in client_diagram_data]
        title = 'Top 10 Tariffs by Total Price'
    else:
        labels = [country['billing_country__name'] for country in country_turnover_data]
        values = [country['turnover'] for country in country_turnover_data]
        title = 'Turnover by Country'

    # Create pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # Update graph layout
    fig.update_layout(title=title)

    return fig


@app.callback(
    Output('client-table', 'data'),
    [Input('data-type-dropdown', 'value'),
     Input('search_clients', 'value')]
)
def update_client_table(selected_data_type, search_query):
    """ Update the client table """

    # Calculate turnover data
    _, client_turnover_data, _ = calculate_turnover()

    # Prepare data for the client table
    client_table_data = [{'client__username': client['client__username'],
                          'client__email': client['client__email'],
                          'turnover': client['turnover']}
                         for client in client_turnover_data]

    # Filter data based on search query
    if search_query:
        client_table_data = [client for client in client_table_data
                             if search_query.lower() in client['client__username'].lower()
                             or search_query.lower() in client['client__email'].lower()]

    return client_table_data


@app.callback(
    Output('country-table', 'data'),
    [Input('data-type-dropdown', 'value'),
     Input('search_country', 'value')]
)
def update_country_table(selected_data_type, search_query):
    """ Update the country table """

    # Calculate turnover data
    _, _, country_turnover_data = calculate_turnover()

    # Prepare data for the country table
    country_table_data = [
        {'billing_country__name': country['billing_country__name'], 'turnover': country['turnover']}
        for country in country_turnover_data
    ]

    # Filter data based on search query
    if search_query:
        country_table_data = [country for country in country_table_data
                              if search_query.lower() in country['billing_country__name'].lower()]

    return country_table_data
