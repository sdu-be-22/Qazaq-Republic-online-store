from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', index, name='user_index'),
    path('update/', user_update, name='user_update'),
]