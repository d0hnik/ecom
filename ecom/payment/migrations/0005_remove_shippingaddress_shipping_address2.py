# Generated by Django 5.0.6 on 2024-08-08 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_order_shipped'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='shipping_address2',
        ),
    ]
