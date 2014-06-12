from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from orders.models import Order, OrderedItem
from orders.serializers import OrderSerializer, OrderedItemSerializer
from products.models import Product

from orders import config

@api_view(['GET', 'POST'])
def order_list(request, format=None):
  """
  List all orders, or create a new order.
  """
  if request.method == 'GET':
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    order = Order()
    order.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'POST'])
def order_detail(request, id, format=None):
  """
  Retrieve, update or delete a order instance.
  """
  try:
    order = Order.objects.get(id=id)
  except Order.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    order_serializer = OrderSerializer(order)
    try:
      ordered_item = OrderedItem.objects.filter(order_id=order)
    except OrderedItem.DoesNotExist:
      return Response(order_serializer.data)
    ordered_item_serializer = OrderedItemSerializer(ordered_item, many=True)
    return Response([order_serializer.data] + ordered_item_serializer.data)

  elif request.method == 'POST':
    if order.status in (
        config.ORDER_CANCELED, config.ORDER_PAID, config.ORDER_PLACED):
      return Response(
          'No modification to ordered items allowed',
          status=status.HTTP_400_BAD_REQUEST)
    try:
      if 'product_id' in request.DATA:
        product = Product.objects.get(id=request.DATA['product_id'])
      elif 'name' in request.DATA:
        product = Product.objects.get(name=request.DATA['name'])
    except Product.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    if 'quantity' in request.DATA:
      ordered_item = OrderedItem(
          order_id=order, product_id=product, quantity=request.DATA['quantity'])
    else:
      ordered_item = OrderedItem(order_id=order, product_id=product)
    ordered_item.save()
    product.ordered = True
    product.save()
    serializer = OrderedItemSerializer(ordered_item)
    return Response(serializer.data)

  elif request.method == 'PUT':
    if 'date' in request.DATA:
      order.date = request.DATA['date']
    if 'status' in request.DATA:
      current_status = ordered_item.status
      new_status = request.DATA['status']
      if current_status != new_status:
        status = (current_status, new_status)
        if status == (config.ORDER_DRAFT, config.ORDER_PLACED):
          if not order_item:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif status == (config.ORDER_DRAFT, config.ORDER_CANCELED):
          if 'reason' not in request.DATA or not request.DATA['reason']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif status == (config.ORDER_PLACED, config.ORDER_PAID):
          pass
        elif status == (config.ORDER_PLACED, config.ORDER_CANCELED):
          if 'reason' not in request.DATA or not request.DATA['reason']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
          return Response(status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
    order.save()
    order_serializer = OrderSerializer(order)
    try:
      ordered_item = OrderedItem.objects.filter(order_id=order)
    except OrderedItem.DoesNotExist:
      return Response(status=status.HTTP_204_NO_CONTENT)
    ordered_item_serializer = OrderedItemSerializer(ordered_item, many=True)
    return Response([order_serializer.data] + ordered_item_serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def ordered_item_detail(request, order_id, product_id, format=None):
  """
  Retrieve, update or delete a order instance.
  """
  try:
    order = Order.objects.get(id=order_id)
  except Order.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  try:
    product = Product.objects.get(id=product_id)
  except Product.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  try:
    ordered_item = OrderedItem.objects.get(order_id=order, product_id=product)
  except OrderedItem.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = OrderedItemSerializer(ordered_item)
    return Response(serializer.data)

  elif request.method == 'PUT':
    if order.status in (
        config.ORDER_CANCELED, config.ORDER_PAID, config.ORDER_PLACED):
      return Response(
          'No modification to ordered items allowed',
          status=status.HTTP_400_BAD_REQUEST)
    if 'quantity' in request.DATA:
      ordered_item.quantity = request.DATA['quantity']
    ordered_item.save()
    serializer = OrderedItemSerializer(ordered_item)
    return Response(serializer.data)

  elif request.method == 'DELETE':
    if order.status in (
        config.ORDER_CANCELED, config.ORDER_PAID, config.ORDER_PLACED):
      return Response(
          'No modification to ordered items allowed',
          status=status.HTTP_400_BAD_REQUEST)
    ordered_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
