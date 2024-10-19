from django.urls import path, include
from .views import Login, Callback, Uninstall, ProductList

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('shopify-callback/', Callback.as_view(), name='callback'),
    path('uninstall/', Uninstall.as_view(), name='uninstall'),

    path('products/', ProductList.as_view(), name='product-list'),
]