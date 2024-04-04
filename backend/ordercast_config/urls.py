"""
URL configuration for ordercast_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from ordercast_product import views

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', views.best_selling_products, name='best_selling_products'),
    path('turnover/', views.turnover, name='turnover'),
    path('best_colors/', views.best_colors, name='best_colors'),

    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
