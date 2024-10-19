from django.urls import path, include
from .views import Login, Callback, Uninstall

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('shopify-callback/', Callback.as_view(), name='callback'),
    path('uninstall/', Uninstall.as_view(), name='uninstall'),
]