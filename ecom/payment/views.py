from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import ShippingAddress, Order, OrderItem
from .forms import ShippingForm, PaymentForm
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        # Get the order items
        order_items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # Check if True or False
            if status == 'true':
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, "Tellimus muudetud!")
            return redirect('home')
        else:
            return render(request, 'payment/orders.html', {"order": order, "items": order_items})
    else:
        messages.error(request, 'Access denied')
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, 'payment/not_shipped_dash.html', {"orders": orders})
    else:
        messages.error(request, 'Access denied')
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, 'payment/shipped_dash.html', {"orders": orders})
    else:
        messages.error(request, 'Access denied')
        return redirect('home')


def get_tax(totals):
    return round(float(totals) * 0.18, 2)


def process_order(request):
    if request.POST:
        cart = Cart(request)
        products = cart.get_prods()
        quantities = cart.get_quantities()
        totals = cart.get_totals()
        # Get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        # Get shipping session data
        my_shipping = request.session.get('my_shipping')
        print(my_shipping)
        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        amount_paid = totals
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        if request.user.is_authenticated:
            # Logged in
            user = request.user
            # Create order
            create_order = Order(user=user, shipping_address=shipping_address, full_name=full_name, email=email,
                                 amount_payed=amount_paid)
            create_order.save()

            # Add order Items
            # Get the order ID
            order_id = create_order.pk
            # Get product info
            for product in products:
                # Get product ID
                product_id = product.id
                # Get the product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get quantity
                for key, value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user,
                                                      quantity=value, price=price)
                        create_order_item.save()
            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            # Delete cart from DB (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete cart
            current_user.update(old_cart="")



        else:
            # Not logged in
            create_order = Order(shipping_address=shipping_address, full_name=full_name, email=email,
                                 amount_payed=amount_paid)
            create_order.save()
            # Add order Items
            # Get the order ID
            order_id = create_order.pk
            # Get product info
            for product in products:
                # Get product ID
                product_id = product.id
                # Get the product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get quantity
                for key, value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id,
                                                      quantity=value, price=price)
                        create_order_item.save()
            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

        messages.success(request, 'Your order has been placed')
        return redirect('home')
    else:
        print("Shit")
        messages.error(request, "Access denied")
        return redirect('home')


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        products = cart.get_prods()
        quantities = cart.get_quantities()
        totals = cart.get_totals()

        # Create a session with Shipping Info
        my_shipping = request.POST
        print(my_shipping)
        request.session['my_shipping'] = my_shipping

        # Check to see if User is logged in
        if request.user.is_authenticated:
            # Get the billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',
                          {"products": products, "quantities": quantities, "totals": totals,
                           "shipping_info": request.POST, "billing_form": billing_form})
        else:
            # Not logged in
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',
                          {"products": products, "quantities": quantities, "totals": totals,
                           "shipping_info": request.POST, "billing_form": billing_form})
    else:
        messages.success(request, "Access denied")
        return redirect('home')


def checkout(request):
    cart = Cart(request)
    products = cart.get_prods()
    quantities = cart.get_quantities()
    totals = cart.get_totals()
    taxes = get_tax(totals)

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html',
                      {"products": products, "quantities": quantities, "totals": totals,
                       "shipping_form": shipping_form, "taxes": taxes})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html',
                      {"products": products, "quantities": quantities, "totals": totals,
                       "shipping_form": shipping_form, "taxes": taxes})


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})
