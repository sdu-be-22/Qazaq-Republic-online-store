import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .utils import *

app_name = 'bastama'


def index(request):
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
        return render(request, 'bastama/index.html', {'title': 'Qazaq Republic'})


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
    basket_data = get_basket_data(request)  # Getting all products from basket
    print(basket_data)
    return render(request, 'bastama/basket.html')


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


def lookbook(request):
    return render(request, 'bastama/lookbook.html')


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
    product_attr, _ = ProductAttribute.objects.get_or_create(product__slug=data.get('product'),
                                                             color__name=data.get('color'))

    if data.get('size'):
        size = Size.objects.get(size_code=data.get('size'))

    order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    print(order)

    order_item = OrderItem.objects.create(order=order, product_attr=product_attr)
    order_item.size = size
    order_item.quantity = data.get('quantity', 1)
    order_item.save()

    return JsonResponse('Successfully added', safe=False)


