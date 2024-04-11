from django.urls import path
from .views import *

urlpatterns = [
    path('products',productsView),
    path('login', login),
    path('logout', logout),
    path('product', createProd),
    path('product/<int:pk>', changeProduct),
    path('cart', getCarts),
    path('cart/<int:pk>', changeCarts),
    path('order', orderChange)
]