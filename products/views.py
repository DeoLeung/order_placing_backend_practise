from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer


@api_view(['GET', 'POST'])
def product_list(request, format=None):
  """
  List all products, or create a new product.
  """
  if request.method == 'GET':
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    if 'id' in request.DATA:
      del request.DATA['id']
    if 'ordered' in request.DATA:
      del request.DATA['ordered']
    serializer = ProductSerializer(data=request.DATA)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id, format=None):
  """
  Retrieve, update or delete a product instance.
  """
  try:
    product = Product.objects.get(id=id)
  except Product.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = ProductSerializer(product)
    return Response(serializer.data)

  elif request.method == 'PUT':
    if 'ordered' in request.DATA:
      del request.DATA['ordered']
    serializer = ProductSerializer(product, data=request.DATA, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    if product.ordered:
      return Response('Cannot delete ordered product')
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
