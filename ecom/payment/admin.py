from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register the model on the admin section

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


# Create and OrderItem Inline

class OrderItemInLine(admin.StackedInline):
    model = OrderItem
    extra = 0


# Extend our Order Model

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    # You can show only fields you want, if you leave it blank, it will show all fieldz
    # fields = ['user', 'full_name']
    inlines = [OrderItemInLine]


# Unregister Order Model
admin.site.unregister(Order)
# Re register our Order and OrderAdmin
admin.site.register(Order, OrderAdmin)
