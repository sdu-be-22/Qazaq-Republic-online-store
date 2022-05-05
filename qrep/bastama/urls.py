from django.urls import path
from .views import *

app_name = 'bastama'

urlpatterns = [
    path('', index, name='home'),
    path('category/<str:cat_name>/', category_products, name='category_products'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('search/', search, name='search'),
    path('favorite/', favorite_products, name='favorite'),
    path('basket/', basket, name='basket'),
    path('update_like/', clicked_favorite_button, name='click_like'),

    path('lookbook/', lookbook, name='lookbook'),

    path('basket_add/', add_product_to_basket, name='add_to_basket'),

    # path('update_favs/<slug:slug>/', click_like, name='click_like'),
    # path('test/', test, name='test'),
]
