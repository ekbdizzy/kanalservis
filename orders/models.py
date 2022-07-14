from django.core.validators import MinValueValidator
from django.db import models


class Order(models.Model):
    number = models.PositiveIntegerField('№', unique=True, db_index=True)
    order_number = models.PositiveIntegerField('Заказ №', unique=True, db_index=True)
    dollar_price = models.DecimalField(
        'Стоимость,$',
        decimal_places=0,
        max_digits=9,
        validators=[MinValueValidator(1)],
    )
    rubble_price = models.DecimalField(
        'Стоимость, руб.',
        decimal_places=2,
        max_digits=11,
        validators=[MinValueValidator(1)],
    )
    delivery_date = models.DateField('Дата поставки')

