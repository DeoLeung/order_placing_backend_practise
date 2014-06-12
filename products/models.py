from django.core import validators
from django.db import models

class Product(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(
      'the name of the product',
      max_length=100, unique=True)
  net_price = models.DecimalField(
      'the price before vat',
      # maximum 99999.99
      max_digits=7, decimal_places=2,
      # default 0.00
      default=0.00,
      # no less than 0.00
      validators=[validators.MinValueValidator(0.00)])
  ordered = models.BooleanField(
      'whether the product has been ordered before',
      default=False)
