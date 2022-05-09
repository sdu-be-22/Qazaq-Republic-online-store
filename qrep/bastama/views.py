import json
import datetime

from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .utils import *

app_name = 'bastama'


def index(request):
    context = general_context(request, 'Qazaq Republic')
    context['lookbooks'] = LookBook.objects.order_by('updated')[:3]

    if request.method == "POST":
        if 'message-ems' in request.POST:
            message_email = request.POST['message-ems']
            send_mail(
                'Direct',
                'subscription from ' + message_email,
                message_email,
                ['200103223@stu.sdu.edu.kz'],
            )
            return redirect("bastama:home")

        else:
            message_email = request.POST['message-email']
            message_name = request.POST['message-name']
            message = request.POST['message']

            send_mail(
                'message from ' + message_name + ',' + message_email,
                message,
                message_email,
                ['200103223@stu.sdu.edu.kz'],
            )
            return redirect("bastama:home")

    else:
        return render(request, 'bastama/index.html', context)


def category_products(request, cat_name):
    context = general_context(request, cat_name.capitalize())

    products_from_subcategory = SIDEBAR_SUBCATEGORY_PRODUCTS[cat_name]
    template_url = get_template_url_for_category(cat_name)

    for product_tuple in products_from_subcategory:
        context_key = product_tuple[0]
        value_to_filter = product_tuple[1]
        context[context_key] = Product.objects.filter(category__name=value_to_filter)

    return render(request, template_url, context)


def product_detail(request, slug):
    context = general_context(request)
    context['data'] = Product.objects.get(slug=slug)
    context['title'] = context.get('data').name

    if context.get('data').size:
        context['sizes'] = Size.objects.all()

    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        _, is_fav = is_favorite_of_customer(customer, context['data'])
        context['is_favorite_product'] = is_fav
        context['user'] = customer
    else:
        context['is_favorite_product'] = False
        context['user'] = None

    return render(request, 'bastama/views/product.html', context)


@login_required(login_url='/account/login/')
def basket(request):
    context = general_context(request, 'Basket')

    customer, _ = Customer.objects.get_or_create(user=request.user)
    order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    context['order_items'] = OrderItem.objects.filter(order=order)
    context['order'] = order

    return render(request, 'bastama/basket.html', context)


@login_required(login_url='/account/login/')
def favorite_products(request):
    context = general_context(request, 'Favorite Products')

    customer, _ = Customer.objects.get_or_create(user=request.user)
    context['favorites'] = Favors.objects.filter(customer=customer)

    return render(request, 'bastama/views/favorite_products.html', context)


@login_required(login_url='/account/login/')
def list_orders(request):
    context = general_context(request, 'My Orders')
    context['orders'] = Order.objects.filter(customer=context['customer']).order_by('-date_ordered')

    return render(request, 'bastama/views/list_order.html', context)


def search(request):
    context = general_context(request, 'Search')

    if request.method == 'POST':
        context['products'] = Product.objects.filter(name__contains=request.POST['search'],
                                                     category__name__contains=request.POST['search'])
    return render(request, 'bastama/search.html', context)


def lookbook(request, pk):
    context = general_context(request)
    lookbook = LookBook.objects.get(pk=pk)
    context['lookbook'] = lookbook
    context['title'] = lookbook.name
    context['sizes'] = Size.objects.all()

    return render(request, 'bastama/lookbook.html', context)


def checkout_order(request):
    context = general_context(request, 'Checkout')
    customer = Customer.objects.get(user=request.user)
    context['order'] = Order.objects.get(customer=customer, complete=False)
    context['order_items'] = OrderItem.objects.filter(order=context.get('order'))

    return render(request, 'bastama/views/checkout.html', context)


def pay_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    shipping_info = data.get('shipping')
    payment_info = data.get('payment')
    customer = Customer.objects.get(user=request.user)
    order = Order.objects.get(customer=customer, complete=False)
    order.transaction = transaction_id

    try:
        payment = Payment.objects.get(customer=customer,
                                      cc_number=payment_info.get('credit_card'),
                                      cc_expiry=payment_info.get('expire'),
                                      cc_code=payment_info.get('ccv'))
    except ObjectDoesNotExist:
        payment = Payment.objects.create(customer=customer)
    finally:
        payment.cc_number = payment_info.get('credit_card')
        payment.cc_expiry = payment_info.get('expire')
        payment.cc_code = payment_info.get('ccv')
        payment.save()

    shipping_address = ShippingAddress.objects.create(customer=customer, order=order)
    shipping_address.address = shipping_info.get('address')
    shipping_address.city = shipping_info.get('city')
    shipping_address.zipcode = shipping_info.get('zipcode')
    shipping_address.save()

    order.complete = True
    order.save()

    return JsonResponse('Successfully ordered', safe=False)


def clicked_favorite_button(request):

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'false', 'message': 'You are not authenticated'}, status=401)

    data = json.loads(request.body)
    customer = Customer.objects.get(user=request.user)
    product = Product.objects.get(slug=data['product_slug'])

    if data['action'] == 'add':
        Favors.objects.create(customer=customer, product=product)
        return JsonResponse('Successfully added', safe=False)
    elif data['action'] == 'remove':
        Favors.objects.get(customer=customer, product=product).delete()
        return JsonResponse('Successfully removed', safe=False)

    return JsonResponse('Error occur', safe=False)


def add_product_to_basket(request):
    data = json.loads(request.body)
    customer, _ = Customer.objects.get_or_create(user=request.user)

    try:
        product_attr = ProductAttribute.objects.get(product__slug=data.get('product'),
                                                    color__name=data.get('color'))
    except ObjectDoesNotExist:
        product = get_object_or_404(Product, slug=data.get('product'))
        color = None

        if data.get('color'):
            color = get_object_or_404(Color, name=data.get('color'))

        product_attr = ProductAttribute.objects.create(product=product, color=color)

    size = None
    if data.get('size'):
        size = Size.objects.get(size_code=data.get('size'))

    order, _ = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product_attr=product_attr, size=size)

    if not created:
        order_item.quantity += int(data.get('quantity', 1))
    else:
        order_item.quantity = int(data.get('quantity', 1))

    order_item.save()

    return JsonResponse('Successfully added', safe=False)


def update_item_quantity(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    order_item = OrderItem.objects.get(pk=product_id)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)
    elif action == 'delete':
        order_item.delete()
        return JsonResponse('Item was deleted', safe=False)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


def look_to_basket(request):
    data = json.loads(request.body)
    lookbook = LookBook.objects.get(pk=data.get('lookbook'))
    looktar = lookbook.lookwithproduct_set.all()
    customer = Customer.objects.get(user=request.user)
    order = Order.objects.get(customer=customer, complete=False)
    size = Size.objects.get(size_code=data.get('size'))

    for look in looktar:
        if look.product_attr.product.size:
            order_item, created = OrderItem.objects.get_or_create(order=order,
                                                                  product_attr=look.product_attr,
                                                                  size=size)
        else:
            order_item, created = OrderItem.objects.get_or_create(order=order,
                                                                  product_attr=look.product_attr)

        if not created:
            order_item.quantity += int(data.get('quantity', 1))
        else:
            order_item.quantity = int(data.get('quantity', 1))
        order_item.save()

    return JsonResponse('Success', safe=False)
