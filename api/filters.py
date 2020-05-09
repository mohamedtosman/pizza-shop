"""
Filters
"""

from django_filters import rest_framework as filters

from .models import Order


class OrderFilter(filters.FilterSet):
    """
    Order Filter
    """
    customer = filters.UUIDFilter(field_name='customer_info__customer')

    class Meta:
        model = Order
        fields = ('customer', 'status')
