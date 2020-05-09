"""
Views
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from .filters import OrderFilter
from .models import Order, Pizza
from .serializers import (OrderSerializer, OrderStatusSerializer,
                          PizzaSerializer)


class OrderViewSet(viewsets.ModelViewSet):
    """
    create:
        Create a new order.
    list:
        Return list of all orders.
    retrieve:
        Return order details using order id.
    update:
        Update order details using order id.
    partial_update:
        Update order details using order id.
    destroy:
        Delete order using order id.
    """
    queryset = Order.objects.select_related(
        'customer_info__customer').prefetch_related(
            'pizzas__pizza').prefetch_related('pizzas__details')
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter

    def partial_update(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class OrderStatusView(generics.RetrieveUpdateAPIView):
    """
    retrieve:
        Return order status for specific order id
    update:
        Update order status for specific order id.
    partial_update:
        Update order status for specific order id.
    """
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer


class PizzaViewSet(viewsets.ModelViewSet):
    """
    create:
        Create new pizza flavor.
    list:
        Return list of all pizza flavors.
    retrieve:
        Return pizza name using pizza id.
    update:
        Update pizza name using pizza id.
    partial_update:
        Update pizza name using pizza id.
    destroy:
        Delete pizza flavor using pizza id.
    """
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
