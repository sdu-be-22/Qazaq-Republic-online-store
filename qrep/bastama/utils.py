from django.core.exceptions import ObjectDoesNotExist

from .models import *
from accounts.models import UserProfile

# Sidebar category seperated by their subcategory
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

TEMPLATE_URL = {
    'jeans': 'bastama/jeans.html',
    'jeide': 'bastama/jeide.html',
    'qosymsha': 'bastama/qosymsha.html',
    'gift': 'bastama/gift.html',
}


def general_context(request, title=None):
    context = dict()
    context['title'] = title

    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
    else:
        customer = None
        profile = None

    context['customer'] = customer
    context['profile'] = profile

    return context


def get_favorite_products(request):
    """
    Get favorite products of customer.
    """
    customer = Customer.objects.get_or_create(user=request.user)
    favorite_products = customer.favors_set.all()

    return favorite_products


def is_favorite_of_customer(customer, favorite_product):
    """
    Looking specific product is favorite of customer or not.
    """
    try:
        customer_favorite = Favors.objects.get(customer=customer, product=favorite_product)
    except ObjectDoesNotExist:
        customer_favorite = None

    return customer_favorite, customer_favorite is not None


def get_template_url_for_category(cat_name):
    """
    Get template by their category name.
    """
    return TEMPLATE_URL[cat_name]
