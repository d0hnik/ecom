from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django.contrib.auth.models import User
from django.db.models import Q
import json
from cart.cart import Cart


def admin_panel(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, "admin.html", {})
    else:
        messages.error(request, "Error occured, try again.")
        return render(request, "home.html", {})


def search(request):
    # Determine if the filled out the form
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # Test for null
        if not searched:
            messages.error(request, "Couldn't find the product. Please try again")
            return render(request, "home.html", {})
        else:
            return render(request, "category.html", {'products': searched})
    else:
        messages.error(request, "Error occured, try again.")
        return render(request, "home.html", {})


def update_info(request):
    if request.user.is_authenticated:
        # Get current's user shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get Users shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if shipping_form.is_valid():
            shipping_form.save()
            messages.success(request, "Your info has been updated!")
            return redirect('home')
        return render(request, "update_info.html", {"shipping_form": shipping_form})
    else:
        messages.error(request, "You are not logged in!")
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did the fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated, Please login again.')
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {"form": form})
    else:
        messages.error(request, "You are not logged in!")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "Your account has been updated!")
            return redirect('home')
        return render(request, "update_user.html", {"user_form": user_form})
    else:
        messages.error(request, "You are not logged in!")
        return redirect('home')


def category(request, foo: str):
    foo = foo.replace("-", " ")
    # Grab the category from the url
    try:
        if foo == 'sale':
            products = Product.objects.filter(is_sale=True)
            sale_percentages = get_sale_percentages(products)
            return render(request, 'category.html', {"products": products, "sale_percentages": sale_percentages})
        else:
            # Look up the category
            category = Category.objects.get(name=foo)
            products = Product.objects.filter(category=category)
            sale_percentages = get_sale_percentages(products)
        return render(request, 'category.html',
                      {"products": products, 'category': category, "sale_percentages": sale_percentages})
    except:
        messages.error(request, 'That category does not exist')
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    category = Category.objects.get(name=product.category.name)
    similar_products = Product.objects.filter(category=category).exclude(id=product.id)[:4]
    return render(request, 'product.html', {"product": product, 'similar_products': similar_products})


def get_sale_percentages(products):
    sale = {}
    for product in products:
        if product.is_sale:
            sale_percentage = round((1 - product.sale_price / product.price) * 100)
            sale[product.id] = sale_percentage
    return sale


def home(request):
    products = Product.objects.all()
    sale_percentages = get_sale_percentages(products)
    print(sale_percentages)
    return render(request, 'home.html', {"products": products, 'sale_percentages': sale_percentages})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Do some shopping cart stuff
            current_user = Profile.objects.get(user_id=request.user.id)
            saved_cart = current_user.old_cart
            # Convert String to python dictionary
            if saved_cart:
                # Convert to dictionary using json
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'There was an error, please try again')
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Konto on edukalt registreeritud.')
            return redirect('home')
        else:
            messages.error(request, 'Tekkis viga, proovige uuesti.')
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
