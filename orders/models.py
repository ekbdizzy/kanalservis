from django.core.validators import MinValueValidator
from django.db import models


class Order(models.Model):
    number = models.PositiveIntegerField('№', unique=True, db_index=True)
    order_number = models.PositiveIntegerField(
        'Заказ №',
        unique=True,
        db_index=True,
    )
    dollar_price = models.DecimalField(
        'Стоимость, $',
        decimal_places=0,
        max_digits=9,
        validators=[MinValueValidator(1)],
        db_index=True,
    )
    rubble_price = models.DecimalField(
        'Стоимость, руб.',
        decimal_places=2,
        max_digits=11,
        validators=[MinValueValidator(1)],
        db_index=True,
    )
    delivery_date = models.DateField('Дата поставки')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('delivery_date',)

    def __str__(self):
        return f'Заказ № {self.order_number}, стоимость: {self.dollar_price}$'
