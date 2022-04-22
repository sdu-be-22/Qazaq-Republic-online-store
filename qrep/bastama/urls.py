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

    path('lookbook/', lookbook, name='lookbook'),
    path('test/', test, name='test'),

    path('update_favs/<slug:slug>/', click_like, name='click_like'),
]
