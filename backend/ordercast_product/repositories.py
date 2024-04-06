from django.db.models import Count, Sum
from ordercast_product.models import Product


class ColorRepository:
    @staticmethod
    def get_top_colors():
        """ Get top best-selling colors """
        return Product.objects.annotate(num_orders=Count('orders')).order_by('-num_orders')[:5]
