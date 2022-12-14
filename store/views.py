import django
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from .models import Address, Cart, Category, Order, Product, Contact_Us
from .forms import RegistrationForm, AddressForm, ContactForm
import decimal
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator  # for Class Based Views
from django.urls import reverse_lazy


# Create your views here.

def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:3]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/index.html', context)


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/detail.html', context)


def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories': categories})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    categories = Category.objects.filter(is_active=True)
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    #paginator = Paginator(products, 12)
    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)
    return render(request, 'store/category_products.html', context)
    #return render(request, 'store/category_products.html', {'products': products, 'page_obj': page_obj})


class ContactUsView(View):
    def get(self, request):
        form = ContactForm
        return render(request, 'store/contact_us.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'store/confirmation.html')


# Authentication Starts Here

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations! Registration Successful!")
            form.save()
        return render(request, 'account/register.html', {'form': form})


@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'account/profile.html', {'addresses': addresses, 'orders': orders})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'account/add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user = request.user
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Address(user=user, locality=locality, city=city, state=state)
            reg.save()
            messages.success(request, "New Address Added Successfully.")
        return redirect('store:profile')


@login_required
def remove_address(request, id):
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Address removed.")
    return redirect('store:profile')


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is already in Cart or Not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()

    return redirect('store:cart')


@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    # Display Total on Cart Page
    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(0)
    # using list comprehension to calculate total amount based on quantity and shipping
    cp = [p for p in Cart.objects.all() if p.user == user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    # Customer Addresses
    addresses = Address.objects.filter(user=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
    }
    return render(request, 'store/cart.html', context)


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('store:cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('store:cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('store:cart')


@login_required
def checkout(request):
    user = request.user
    amount = decimal.Decimal(0)
    total_amount = decimal.Decimal(0)
    addresses = Address.objects.filter(user=user).first()
    cart_products = Cart.objects.filter(user=user)

    cp = [p for p in Cart.objects.all() if p.user == user]
    if cp:
        for p in cp:
            amount = (p.quantity * p.product.price)
            total_amount += amount
    context = {
        'cart_products': cart_products,
        'amount': amount,
        'total_amount': total_amount,
        'addresses': addresses,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def orders(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    addresses = Address.objects.filter(user=user).first()
    for c in cart:
        # Saving all the products from Cart to Order
        Order(user=user, address=addresses, product=c.product, quantity=c.quantity).save()
        # And Deleting from Cart
        c.delete()
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'store/orders.html', {'orders': all_orders})


def shop(request):
    return render(request, 'store/shop.html')


def test(request):
    return render(request, 'store/test.html')


@permission_required('view_messages', raise_exception=True)
def cust_messages(request):
    all_messages = Contact_Us.objects.all()
    return render(request, 'store/cust_messages.html', {'all_messages': all_messages})


def cust_returns(request):
    return render(request, 'store/cust_returns.html')


def policy(request):
    return render(request, 'store/policy.html')


def faq(request):
    return render(request, 'store/faq.html')


def about_us(request):
    return render(request, 'store/about_us.html')
