from django.urls import path, include
from .views import auth, order, product, compliance

urlpatterns = [
    path('login/', auth.Login.as_view(), name='login'),
    path('shopify-callback/', auth.Callback.as_view(), name='callback'),
    path('uninstall/', auth.Uninstall.as_view(), name='uninstall'),

    path('shopify-webhook/compliance/', compliance.ComplianceWebhook.as_view(), name='webhook_compliance'),

    path('products/', product.ProductList.as_view(), name='product_list'),
    
    path('shopify-webhook/order-create/', order.OrderCreateWebhook.as_view(), name='webhook_order_create'),
    path('orders/', order.OrderList.as_view(), name='order_list'),
]