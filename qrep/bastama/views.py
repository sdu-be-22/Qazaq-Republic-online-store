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

    if request.method == "GET":
        message_email = request.GET['message-ems']

        send_mail(
            'subscription from ' + message_ems,
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
    context['sizes'] = Size.objects.all()
    context['title'] = context['data'].name

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


def click_like(request, slug):
    customer, _ = Customer.objects.get_or_create(user=request.user)
    favorite_product = Product.objects.get(slug=slug)

    favorite, is_fav = is_favorite_of_customer(customer, favorite_product)

    if is_fav:
        favorite.delete()
    else:
        Favors.objects.create(customer=customer, product=favorite_product)

    return redirect('bastama:product_detail', slug=slug)


def test(request):
    context = {'title': 'test'}

    set_product_to_basket(request, context['form'])
    return render(request, 'bastama/components/test.html', context)
