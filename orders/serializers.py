from rest_framework import serializers
from orders.models import Order, OrderedItem


class OrderSerializer(serializers.ModelSerializer):
  net_price = serializers.Field(source='net_price')
  gross_price = serializers.Field(source='gross_price')
  class Meta:
    model = Order
    fields = ('id', 'status', 'vat', 'date', 'net_price', 'gross_price')


class OrderedItemSerializer(serializers.ModelSerializer):
  product_name = serializers.Field(source='product_name')
  product_net_price = serializers.Field(source='product_net_price')
  class Meta:
    model = OrderedItem
    fields = ('id', 'order_id', 'product_id', 'quantity', 'product_name')
