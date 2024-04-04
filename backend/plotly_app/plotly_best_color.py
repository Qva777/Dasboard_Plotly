import plotly.graph_objs as go
from dash import html, dcc
from dash.dependencies import Input, Output

from django_plotly_dash import DjangoDash
from ordercast_product.repositories import ColorRepository

# Create a DjangoDash app
app = DjangoDash('BestColorApp')


def get_top_colors():
    """ Function to get the top 5 colors """

    # Get top 5 colors from db
    top_colors = ColorRepository.get_top_colors()

    colors = [item['color'] for item in top_colors]
    counts = [item['count'] for item in top_colors]
    return colors, counts


# Create initial data
initial_colors, initial_counts = get_top_colors()

# Layout of the app
app.layout = html.Div([
    html.H1('Top 5 Best Colors'),
    dcc.Graph(id='color-bar-chart', figure=go.Figure(data=[go.Bar(x=initial_colors, y=initial_counts)])),
    dcc.Interval(
        id='interval-component',
        interval=60000,  # (60 seconds)
        n_intervals=0
    )
])


@app.callback(Output('color-bar-chart', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    """ Callback to update the graph """
    colors, counts = get_top_colors()
    bar_chart = go.Bar(
        x=colors,
        y=counts,
        marker=dict(color='purple'),
    )
    layout = go.Layout(
        title='Top 5 Best Colors',
        xaxis=dict(title='Color'),
        yaxis=dict(title='Count'),
    )
    fig = go.Figure(data=[bar_chart], layout=layout)
    return fig
