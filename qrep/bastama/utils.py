from .models import *

SIDEBAR_SUBCATEGORY_PRODUCTS = {
    'jeans': [
        ('jeans', 'Jeans'),
        ('shalbars', 'Shalbar')
    ],
    'jeide': [
        ('jeideler', 'Jeide'),
        ('kenjeideler', 'Kenjeide'),
        ('birjeideler', 'Burjeide')
    ],
    'qosymsha': [
        ('betperdeler', 'Betperde'),
        ('botelkeler', 'Botelke'),
        ('keseler', 'Kese'),
        ('qalpaktar', 'Qalpaq'),
        ('panamalar', 'Panama'),
        ('kepkalar', 'Kepka'),
        ('somkeler', 'Somke'),
    ],
    'gift': [
        ('gifts', 'Gift')
    ]
}


def get_basket_data(request):
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        print(customer)
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_basket_total
    else:
        order = []
        items = []
        cart_items = []
        print(request.COOKIES.get('csrftoken'), 'token is here')

    return {'cartItems': cart_items, 'items': items, 'order': order}


def get_favorite_products(request):
    customer = Customer.objects.get_or_create(user=request.user)
    favorite_products = customer.favors_set.all()

    return favorite_products


def is_favorite_of_customer(customer, favorite_product):
    print('before customer favorite')
    try:
        customer_favorite = Favors.objects.get(customer=customer, product=favorite_product)
    except Exception:
        customer_favorite = None

    return customer_favorite, customer_favorite is not None


def get_template_url_for_category(cat_name):
    template_url = 'bastama/'

    if cat_name == 'jeans':
        template_url += 'jeans.html'
    elif cat_name == 'jeide':
        template_url += 'jeide.html'
    elif cat_name == 'qosymsha':
        template_url += 'qosymsha.html'
    elif cat_name == 'gift':
        template_url += 'gift.html'

    return template_url


def set_product_to_basket(request, form):
    if request.user.is_authenticated:
        print('axa')
    else:
        print('dolbaeb ti')
