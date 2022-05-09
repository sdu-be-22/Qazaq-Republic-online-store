from django.urls import path
from .views import *

app_name = 'bastama'

urlpatterns = [
    path('', index, name='home'),
    path('category/<str:cat_name>/', category_products, name='category_products'),
    path('lookbook/<int:pk>/', lookbook, name='lookbook'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('basket/', basket, name='basket'),
    path('favorite/', favorite_products, name='favorite'),
    path('search/', search, name='search'),
    path('checkout/', checkout_order, name='checkout'),
    path('my_orders/', list_orders, name='my_orders'),

    # JsonResponse endpoints
    path('paypal/', pay_order, name='paypal'),
    path('update_like/', clicked_favorite_button, name='click_like'),
    path('update_item/', update_item_quantity, name='update_item'),
    path('basket_add/', add_product_to_basket, name='basket_add'),
    path('look_basket/', look_to_basket, name='look_basket'),
]
