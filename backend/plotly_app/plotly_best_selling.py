from django_plotly_dash import DjangoDash
import dash_table
from dash import html, dcc
import plotly.graph_objs as go
from ordercast_client.repositories import ClientRepository
from ordercast_country.repositories import CountryRepository
from ordercast_order.models import Order
from dash.dependencies import Input, Output
from datetime import date

from ordercast_order.repositories import OrderRepository
from plotly_app.style import button_style, input_style, dropdown

# Create a DjangoDash app
app = DjangoDash('BestSelling')

# Country
countries = CountryRepository.get_country_data()
dropdown_countries = [{'label': country.name, 'value': country.code} for country in countries]

# Client
clients = ClientRepository.get_client_data()
dropdown_clients = [{'label': client.tariff_name, 'value': client.tariff_name} for client in clients]

# Order
orders = Order.objects.all().select_related('products', 'client', 'billing_country')
order_data = [
    {
        'ref': order.products.ref,
        'color': order.products.color,
        'tariff_name': order.client.tariff_name,
        'billing_country': order.billing_country.name,
        'created_at': order.created_at
    }
    for order in orders
]

order_client_data = Order.objects.select_related('client', 'products').values(
    'client__username', 'client__email', 'products__ref', 'products__color', 'total', 'created_at'
)

client_data = [
    {
        "username": order["client__username"],
        "email": order["client__email"],
        "ref": order["products__ref"],
        "color": order["products__color"],
        "price": order["total"],
        "created_at": order["created_at"]
    }
    for order in order_client_data
]

client_columns = ["username", "email", "ref", "color", "price"]

client_initial_active_cell = {'row': 0, 'column': 0}

# Layout of the app
app.layout = html.Div(
    [
        html.Br(),
        dcc.Graph(id='table-graph'),
        dcc.DatePickerRange(
            minimum_nights=5,
            clearable=True,
            with_portal=True,
            start_date=date(2017, 6, 21)
        ),

        html.Button('Today', id='btn-nclicks-1', n_clicks=0, style=button_style),
        html.Button('Week', id='btn-nclicks-2', n_clicks=0, style=button_style),
        html.Button('Month', id='btn-nclicks-3', n_clicks=0, style=button_style),
        html.Button('All time', id='btn-nclicks-4', n_clicks=0, style=button_style),

        html.Br(),
        html.H2("Best selling products by merchant"),
        html.Br(),
        html.Div(children=[
            dcc.Input(
                id="search-client",
                type="text",
                placeholder="Hector & Sons",
                style=input_style,
            ),
        ], style={'display': 'flex', 'flexDirection': 'row'}),

        html.Div(children=[
            html.Div(
                [
                    html.Br(),
                    dash_table.DataTable(
                        id="client-table",
                        columns=[{"name": c, "id": c} for c in client_columns],
                        data=client_data,
                        page_size=10,
                        sort_action="native",
                        active_cell=client_initial_active_cell,
                    )
                ],
            ),
        ]),

        html.Br(),
        html.H2("Best selling products by country and price rates"),
        html.Br(),
        html.Div(children=[
            dcc.Input(
                id="search-input",
                type="text",
                placeholder="Search by product",
                style=input_style,
            ),
            dcc.Dropdown(
                id='country-dropdown',
                options=dropdown_countries,
                multi=True,
                placeholder="Select country",
                style=dropdown,
            ),
            dcc.Dropdown(
                id='tariff-dropdown',
                options=dropdown_clients,
                multi=True,
                placeholder="All price rates",
                style=dropdown,
            ),
        ], style={'display': 'flex', 'flexDirection': 'row'}),

        html.Div(children=[
            html.Div([
                dash_table.DataTable(
                    id="table",
                    columns=[{"name": c, "id": c} for c in
                             ["ref", "color", "tariff_name", "billing_country", "created_at"]],
                    data=order_data,
                    page_size=10,
                    sort_action="native",
                    filter_action="native",
                ),
            ], style={'margin-top': '15px'}),
        ]),

    ]
)


@app.callback(
    Output('table-graph', 'figure'),
    [Input('table', 'active_cell')]
)
def update_figure(active_cell):
    """ Short info about user in the table """

    # Request to db
    user_data = OrderRepository.get_user_data()

    users_count = user_data['users_count']
    users_approved_count = user_data['users_approved_count']
    users_with_orders_count = user_data['users_with_orders_count']
    orders_count = user_data['orders_count']
    total_turnover = user_data['total_turnover']

    # Create header and cell values for the table
    header_values = ['Users', 'Users approved', 'Users with orders', 'Amount of orders', 'Turnover']
    cell_values = [
        [users_count],
        [users_approved_count],
        [users_with_orders_count],
        [orders_count],
        [total_turnover],
    ]

    # Generate the table figure
    fig = go.Figure(data=[go.Table(
        header=dict(values=header_values),
        cells=dict(values=cell_values)
    )])

    fig.update_layout(height=240)
    return fig


@app.callback(
    Output("table", "data"),
    [Input("search-input", "value"),
     Input("country-dropdown", "value"),
     Input("tariff-dropdown", "value")]
)
def update_table(search_query, selected_countries, selected_tariff):
    filtered_data = order_data

    if search_query:
        search_query_lower = search_query.lower()
        filtered_data = [
            order for order in filtered_data
            if search_query_lower in order["ref"].lower()
        ]

    if selected_countries:
        selected_country_labels = [option['label'] for option in dropdown_countries if
                                   option['value'] in selected_countries]
        filtered_data = [
            order for order in filtered_data
            if order["billing_country"] in selected_country_labels
        ]

    if selected_tariff:
        selected_tariff_labels = [option['label'] for option in dropdown_clients if option['value'] in selected_tariff]
        filtered_data = [
            order for order in filtered_data
            if order["tariff_name"] in selected_tariff_labels
        ]

    return filtered_data


@app.callback(
    Output("client-table", "data"),
    [Input("search-client", "value"),
     Input("btn-nclicks-1", "n_clicks")]
)
def update_table(search_query, n_clicks):
    print("Search Query:", search_query)

    filtered_data = client_data

    if search_query:
        search_query_lower = search_query.lower()
        filtered_data = [
            client for client in filtered_data
            if search_query_lower in client["username"].lower() or
               search_query_lower in client["email"].lower()
        ]

    #  filter "Today"
    if n_clicks:
        filtered_data = [client for client in filtered_data if client['created_at'].date() == date.today()]

    return filtered_data
