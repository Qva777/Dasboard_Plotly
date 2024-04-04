from django.db.models import Count
from ordercast_product.models import Product


class ColorRepository:
    @staticmethod
    def get_top_colors():
        """ Get top best-selling colors """
        return Product.objects.values('color').annotate(count=Count('color')).order_by('-count')[:5]
