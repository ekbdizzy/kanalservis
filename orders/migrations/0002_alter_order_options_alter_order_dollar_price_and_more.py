# Generated by Django 4.0.6 on 2022-07-14 12:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('delivery_date',), 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='order',
            name='dollar_price',
            field=models.DecimalField(db_index=True, decimal_places=0, max_digits=9, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Стоимость, $'),
        ),
        migrations.AlterField(
            model_name='order',
            name='rubble_price',
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=11, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Стоимость, руб.'),
        ),
    ]
