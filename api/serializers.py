"""
Serializers
"""

from rest_framework import serializers
from .models import (Customer, CustomerInfo, Order,
                     Pizza, PizzaDetail, PizzaOrder)


class CustomerInfoSerializer(serializers.ModelSerializer):
    """
    Customer Info Serializer
    """
    id = serializers.UUIDField(source='customer.id', required=False)
    name = serializers.CharField(source='customer.name')

    class Meta:
        model = CustomerInfo
        fields = ('id', 'name', 'address', 'phone')

    def validate(self, data):
        if self.context['view'].action == 'update':
            if self.parent and self.parent.instance:
                customer = self.parent.instance.customer_info.customer
                name = data['customer']['name']

                if customer.name != name:
                    if Customer.objects.filter(name=name).exists():
                        raise serializers.ValidationError({'name': 'Name already exists.'})
        return data


class PizzaSerializer(serializers.ModelSerializer):
    """
    Pizza Serializer
    """
    class Meta:
        model = Pizza
        fields = ('id', 'name')


class PizzaDetailSerializer(serializers.ModelSerializer):
    """
    Pizza Detail Serializer
    """
    class Meta:
        model = PizzaDetail
        fields = ('size', 'count')


class PizzaOrderSerializer(serializers.ModelSerializer):
    """
    Pizza Order Serializer
    """
    id = serializers.UUIDField(source='pizza.id')
    name = serializers.CharField(source='pizza.name', required=False)
    details = PizzaDetailSerializer(many=True)

    class Meta:
        model = PizzaOrder
        fields = ('id', 'name', 'details')

    def validate(self, data):
        try:
            Pizza.objects.get(id=data['pizza']['id'])
        except Pizza.DoesNotExist:
            raise serializers.ValidationError({'id': 'No pizza is found.'})

        if not data['details']:
            raise serializers.ValidationError({'details': 'This list may not be empty.'})

        sizes = set()
        for detail in data['details']:
            sizes.add(detail['size'])

        if len(data['details']) != len(sizes):
            raise serializers.ValidationError({'details': 'Size is repeated more than once.'})

        return data


class OrderSerializer(serializers.ModelSerializer):
    """
    Order Serializer
    """
    customer = CustomerInfoSerializer(source='customer_info')
    pizzas = PizzaOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'pizzas', 'status', 'delivered', 'delivered_at', 'created_at')
        read_only_fields = ('status', 'delivered', 'delivered_at', 'created_at')

    def validate(self, data):
        if self.instance:
            if not self.instance.can_update():
                raise serializers.ValidationError({'error': 'Cannot update order.'})

        if not data['pizzas']:
            raise serializers.ValidationError({'pizzas': 'This list may not be empty.'})

        pizzas_ids = set()
        for pizza in data['pizzas']:
            pizzas_ids.add(pizza['pizza']['id'])

        if len(data['pizzas']) != len(pizzas_ids):
            raise serializers.ValidationError({'pizzas': 'Pizzas should be aggregated by id.'})

        return data

    def create(self, validated_data):
        customer_data = validated_data.pop('customer_info')
        customer, _ = Customer.objects.get_or_create(name=customer_data['customer']['name'])
        customer_data.pop('customer')
        customer_info, _ = CustomerInfo.objects.get_or_create(customer=customer, **customer_data)
        pizzas_data = validated_data.pop('pizzas')
        order = Order.objects.create(customer_info=customer_info, **validated_data)

        for pizza_data in pizzas_data:
            pizza = Pizza.objects.get(id=pizza_data['pizza']['id'])
            pizza_order = PizzaOrder.objects.create(pizza=pizza, order=order)

            for detail_data in pizza_data['details']:
                PizzaDetail.objects.create(pizza_order=pizza_order, **detail_data)

        return order

    def update(self, instance, validated_data):
        customer_data = validated_data.pop('customer_info')
        customer = instance.customer_info.customer
        if customer.name != customer_data['customer']['name']:
            customer.name = customer_data['customer']['name']
            customer.save()

        instance.customer_info.address = customer_data['address']
        if 'phone' in customer_data:
            instance.customer_info.phone = customer_data['phone']

        instance.customer_info.save()
        instance.pizzas.all().delete()
        for pizza_data in validated_data['pizzas']:
            pizza = Pizza.objects.get(id=pizza_data['pizza']['id'])
            pizza_order = PizzaOrder.objects.create(pizza=pizza, order=instance)

            for detail in pizza_data['details']:
                PizzaDetail.objects.create(pizza_order=pizza_order, **detail)

        return instance


class OrderStatusSerializer(serializers.ModelSerializer):
    """
    Order Status Serializer
    """
    status = serializers.ChoiceField(required=True, choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ('id', 'status', 'delivered', 'delivered_at')
        read_only_fields = ('delivered', 'delivered_at')

    def validate(self, data):
        if self.instance:
            if not self.instance.can_update_status(data['status']):
                raise serializers.ValidationError({'error': 'Cannot update order status.'})

        return data

    def update(self, instance, validated_data):
        instance.update_status(validated_data['status'])
        return instance
