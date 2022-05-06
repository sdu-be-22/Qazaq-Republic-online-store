import json

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
    context = dict()
    context['title'] = 'Qazaq Republic'
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
    context = dict()
    context['title'] = cat_name.capitalize()

    products_from_subcategory = SIDEBAR_SUBCATEGORY_PRODUCTS[cat_name]
    template_url = get_template_url_for_category(cat_name)

    for product_tuple in products_from_subcategory:
        context_key = product_tuple[0]
        value_to_filter = product_tuple[1]
        context[context_key] = Product.objects.filter(category__name=value_to_filter)

    return render(request, template_url, context)


def product_detail(request, slug):
    context = dict()
    context['data'] = Product.objects.get(slug=slug)
    context['title'] = context.get('data').name

    if context.get('data').size:
        context['sizes'] = Size.objects.all()

    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        _, is_fav = is_favorite_of_customer(customer, context['data'])
        context['is_favorite_product'] = is_fav
        context['user'] = customer
        print(context.get('is_favorite_product'), 'from product detail fav')
    else:
        context['is_favorite_product'] = False
        context['user'] = None

    return render(request, 'bastama/views/product.html', context)


def basket(request):
    # basket_data = get_basket_data(request)  # Getting all products from basket
    context = dict()
    context['title'] = 'Basket'

    customer, _ = Customer.objects.get_or_create(user=request.user)
    order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    context['order_items'] = OrderItem.objects.filter(order=order)
    context['order'] = order

    return render(request, 'bastama/basket.html', context)


@login_required(login_url='/accounts/login/')
def favorite_products(request):
    context = dict()
    context['title'] = 'Favorite Products'

    customer, _ = Customer.objects.get_or_create(user=request.user)
    context['favorites'] = Favors.objects.filter(customer=customer)

    return render(request, 'bastama/views/favorite_products.html', context)


def search(request):
    context = dict()
    context['title'] = 'Search'

    if request.method == 'POST':
        context['products'] = Product.objects.filter(name__contains=request.POST['search'],
                                                     category__name__contains=request.POST['search'])

    return render(request, 'bastama/search.html', context)


def lookbook(request, pk):
    context = dict()
    print(pk)
    lookbook = LookBook.objects.get(pk=pk)
    context['lookbook'] = lookbook
    context['title'] = lookbook.name
    context['sizes'] = Size.objects.all()

    return render(request, 'bastama/lookbook.html', context)


def checkout_order(request):
    context = dict()
    order = Order.objects.get_or_create()
    return render(request, 'bastama/views/checkout.html')


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
    except:
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

    # order_item.quantity = data.get('quantity', 1)
    # order_item.save()

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

