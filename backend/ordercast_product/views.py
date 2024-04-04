from django.shortcuts import render

# Plotly it is forbidden to delete !
from plotly_app import plotly_turnover, plotly_best_selling, plotly_best_color


def best_selling_products(request):
    """ Best-selling products """
    return render(request, 'best_selling.html')


def turnover(request):
    """ Turnover Analysis """
    return render(request, 'turnover.html')


def best_colors(request):
    """ Return Top 5 Best Colors """
    return render(request, 'best_color.html')
