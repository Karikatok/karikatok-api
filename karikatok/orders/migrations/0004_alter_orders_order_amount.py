# Generated by Django 5.1.3 on 2024-12-31 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_orders_order_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_amount',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=10),
        ),
    ]
