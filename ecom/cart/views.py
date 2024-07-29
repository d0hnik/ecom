from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    products = cart.get_prods()
    quantities = cart.get_quantities()
    totals = cart.get_totals()
    return render(request, 'cart_summary.html', {"products": products, "quantities": quantities, "totals": totals})


def cart_add(request):
    # Get the cart
    cart = Cart(request=request)
    # Test for Post
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        # Lookup product in db
        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, 'Product added to cart')
        return response


def cart_delete(request):
    cart = Cart(request=request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')

        cart.delete(product_id=product_id)
        response = JsonResponse({'message': "success"})
        messages.success(request, 'Product deleted successfully')
        return response


def cart_update(request):
    cart = Cart(request=request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        if int(product_qty) > 0:
            cart.update(product_id=product_id, quantity=product_qty)
        else:
            cart.delete(product_id=product_id)
        response = JsonResponse({'qty': cart.__len__()})
        messages.success(request, 'Cart updated successfully')
        return response
