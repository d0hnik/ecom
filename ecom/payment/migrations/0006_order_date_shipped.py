# Generated by Django 5.0.6 on 2024-08-12 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_remove_shippingaddress_shipping_address2'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_shipped',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
