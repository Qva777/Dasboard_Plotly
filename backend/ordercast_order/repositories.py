from django.db.models import Sum

from ordercast_order.models import Order

from ordercast_client.models import Client


class OrderRepository:
    @staticmethod
    def client_turnover_data():
        """ Calculate turnover per client """
        return (
            Order.objects
            .values('client__username', 'client__email', 'client__tariff_name')
            .annotate(turnover=Sum('total'))
            .order_by('-turnover')
        )

    @staticmethod
    def country_turnover_data():
        """ Calculate turnover per country """
        return (
            Order.objects
            .values('billing_country__name')
            .annotate(turnover=Sum('total'))
            .order_by('-turnover')
        )

    @staticmethod
    def get_user_data():
        """ User data for table """

        users_count = Client.objects.count()
        users_approved_count = Client.objects.filter(is_approved=True).count()
        users_with_orders_count = Client.objects.filter(order__isnull=False).distinct().count()
        orders_count = Order.objects.count()
        total_turnover = Order.objects.aggregate(Sum('total'))['total__sum']

        return {
            'users_count': users_count,
            'users_approved_count': users_approved_count,
            'users_with_orders_count': users_with_orders_count,
            'orders_count': orders_count,
            'total_turnover': total_turnover,
        }