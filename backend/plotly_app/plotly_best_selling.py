import datetime
import dash_table
import plotly.graph_objs as go

from collections import Counter
from dash import html, dcc
from dash.dependencies import Input, Output
from django.db.models import Q
from django_plotly_dash import DjangoDash

from ordercast_client.repositories import ClientRepository
from ordercast_country.repositories import CountryRepository
from ordercast_order.repositories import OrderRepository
from plotly_app.style import input_style, dropdown

# Create a DjangoDash app
app = DjangoDash('BestSelling')

# Tables
output_sorted_client = []
output_sorted_country = []

# Layout of the app
app.layout = html.Div(
    [
        html.Br(),
        dcc.Graph(id='table-graph'),

        html.Div([
            dcc.Dropdown(
                id='time-filter',
                options=[
                    {'label': 'Today', 'value': 'today'},
                    {'label': 'Week', 'value': 'week'},
                    {'label': 'Month', 'value': 'month'},
                    {'label': 'All Time', 'value': 'all_time'},
                ],
                value='all_time',
                clearable=False,
            )
        ]),

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
                        columns=[
                            {"name": c, "id": c} for c in ["username", "email", "ref", "color", "price", "quantity"]
                        ],
                        data=output_sorted_client,
                        page_size=10,
                        sort_action="native",
                        style_cell=dict(textAlign='center'),

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
                options=[],
                multi=True,
                placeholder="Select country",
                style=dropdown,
            ),

            dcc.Dropdown(
                id='tariff-dropdown',
                options=[],
                multi=True,
                placeholder="All price rates",
                style=dropdown,
            ),

        ], style={'display': 'flex', 'flexDirection': 'row'}),

        html.Div(children=[
            html.Div([
                dash_table.DataTable(
                    id="table",
                    columns=[{"name": c, "id": c} for c in ["ref", "color", "quantity"]],
                    data=output_sorted_country,
                    page_size=10,
                    sort_action="native",
                    filter_action="native",
                    style_cell=dict(textAlign='center'),
                ),
            ], style={'margin-top': '15px'}),
        ]),

    ]
)


@app.callback(Output('table-graph', 'figure'),
              [Input('table', 'active_cell')])
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


def filter_queryset(queryset, search_query=None, selected_countries=None, selected_tariff=None, time_filter=None):
    """ Filter for queryset """

    if search_query:
        queryset = queryset.filter(
            Q(products__ref__icontains=search_query) |
            Q(client__username__icontains=search_query) |
            Q(client__email__icontains=search_query)
        )

    if selected_countries:
        countries = CountryRepository.get_country_data()
        unique_countries = {country.code: country.name for country in countries}
        dropdown_countries = [{'label': name, 'value': code} for code, name in unique_countries.items()]

        selected_country_labels = [
            option['label'] for option in dropdown_countries if option['value'] in selected_countries]

        queryset = queryset.filter(billing_country__name__in=selected_country_labels)

    if selected_tariff:
        queryset = queryset.filter(client__tariff_name__in=selected_tariff)

    if time_filter == "today":
        queryset = queryset.filter(created_at__date=datetime.date.today())
    elif time_filter == "week":
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=6)
        queryset = queryset.filter(created_at__date__range=[start_date, end_date])
    elif time_filter == "month":
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=29)
        queryset = queryset.filter(created_at__date__range=[start_date, end_date])

    return queryset


@app.callback(Output("client-table", "data"),
              [Input("search-client", "value"),
               Input("time-filter", "value")])
def update_table_client(search_query, time_filter):
    """ When the page reloads, also reloads the table """

    # Construct base queryset
    queryset = OrderRepository.get_related_client()

    # Filter the queryset
    queryset = filter_queryset(queryset, search_query=search_query, time_filter=time_filter)

    # Group the data by 'client__username' and 'products__ref'
    counts_client = Counter((entry["client__username"], entry["products__ref"]) for entry in queryset)

    # Construct the output list with grouped products, their quantities, and the total amount
    output_client = [
        {
            "username": username,
            "email": next(entry["client__email"] for entry in queryset if
                          (entry["client__username"], entry["products__ref"]) == group),
            "ref": ref,
            "color": next(entry["products__color"] for entry in queryset if
                          (entry["client__username"], entry["products__ref"]) == group),
            "price": sum(float(entry["total"]) for entry in queryset if
                         (entry["client__username"], entry["products__ref"]) == group),
            "quantity": str(count)
        }
        for group, count in counts_client.items()
        for username, ref in [group]
    ]

    # Sort the output list by quantity in descending order
    output_sorted_clients = sorted(output_client, key=lambda x: int(x["quantity"]), reverse=True)

    return output_sorted_clients


@app.callback([
    Output('country-dropdown', 'options'),
    Output('tariff-dropdown', 'options')],
    [Input('country-dropdown', 'value'),
     Input('tariff-dropdown', 'value')])
def update_dropdowns(selected_countries, selected_tariffs):
    """ When the page reloads, also reloads the dropdown """

    # Update options for country dropdown
    countries = CountryRepository.get_country_data()
    unique_countries = {country.code: country.name for country in countries}
    dropdown_countries = [{'label': name, 'value': code} for code, name in unique_countries.items()]

    # Update options for tariff dropdown
    clients = ClientRepository.get_client_data()
    unique_tariffs = {client.tariff_name: client.tariff_name for client in clients}
    dropdown_clients = [{'label': name, 'value': name} for name in unique_tariffs]

    return dropdown_countries, dropdown_clients


@app.callback(
    Output("table", "data"),
    [Input("search-input", "value"),
     Input("country-dropdown", "value"),
     Input("tariff-dropdown", "value"),
     Input("time-filter", "value")])
def update_table_country(search_query, selected_countries, selected_tariff, time_filter):
    """ When the page reloads, also reloads the table """

    # Construct base queryset
    queryset = OrderRepository.get_related_country()

    # Filter the queryset
    queryset = filter_queryset(queryset, search_query, selected_countries, selected_tariff, time_filter)

    # Retrieve filtered data
    filtered_data = [
        {
            'ref': order.products.ref,
            'color': order.products.color,
            'tariff_name': order.client.tariff_name,
            'billing_country': order.billing_country.name,
        }
        for order in queryset
    ]

    # Count occurrences of each unique combination of 'ref', 'tariff_name', and 'billing_country'
    counts = Counter((d['ref'], d['tariff_name'], d['billing_country']) for d in filtered_data)

    # Construct the output list with grouped products and their quantities
    output_country = [
        {
            'ref': ref,
            'color': next(
                d['color'] for d in filtered_data if (d['ref'], d['tariff_name'], d['billing_country']) == group),
            'quantity': str(count)
        }
        for group, count in counts.items()
        for ref, tariff_name, billing_country in [group]
    ]

    # Sort the output list by quantity in descending order
    output_sorted_countries = sorted(output_country, key=lambda x: int(x['quantity']), reverse=True)

    return output_sorted_countries
