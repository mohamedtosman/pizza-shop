"""
Urls
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'api'

ROUTER = DefaultRouter()
ROUTER.register(r'orders', views.OrderViewSet, basename='orders')
ROUTER.register(r'pizzas', views.PizzaViewSet, basename='pizzas')

urlpatterns = ROUTER.urls + [
    path('orders/<uuid:pk>/status/',
         views.OrderStatusView.as_view(), name='order-status')
]
