from django.core import validators
from django.db import models
from django.utils import timezone

from orders import config
from products.models import Product

class Order(models.Model):
  id = models.AutoField(primary_key=True)
  status = models.CharField(
      'the status of the order',
      max_length=10,
      choices=config.ORDER_STATUS,
      default=config.ORDER_DRAFT)
  vat = models.DecimalField(
      'the vat of the order',
      max_digits=3, decimal_places=2,
      default=config.VAT,
      # between 0.00 and 100.00 inclusive
      validators=[validators.MinValueValidator(0.00),
                  validators.MaxValueValidator(100.00)])
  date = models.DateTimeField('date of order created', default=timezone.now())

  def net_price(self):
    price = 0.0
    try:
      items = OrderedItem.objects.filter(order_id=self)
    except OrderedItem.DoesNotExist:
      return price
    for item in items:
      price += float(item.quantity * item.product_net_price())
    return price

  def gross_price(self):
    # TODO: this fixed the vat at creation.
    return self.net_price() * (1 + float(self.vat))

class OrderedItem(models.Model):
  id = models.AutoField(primary_key=True)
  order_id = models.ForeignKey(Order)
  product_id = models.ForeignKey(Product)
  quantity = models.IntegerField(
      'the quantity of the product',
      default=1,
      validators=[validators.MinValueValidator(1)])

  def product_name(self):
    return self.product_id.name

  def product_net_price(self):
    return self.product_id.net_price
