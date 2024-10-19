from django.conf import settings

from rest_framework.response import Response
from rest_framework import status

from shopify.utils import shop_url

import binascii
import os
import shopify


def authenticate(request):
    try:
        shop = get_sanitized_shop_param(request)
        scopes, redirect_uri, state = build_auth_params()
        
        request.session["shopify_oauth_state_param"] = state

        permission_url = _new_session(shop).create_permission_url(
            scopes, redirect_uri, state
        )
        return Response({"url": permission_url, "shopify_oauth_state_param": state}, status=status.HTTP_200_OK)
    
    except ValueError as exception:
        return Response({"error": str(exception)}, status=status.HTTP_400_BAD_REQUEST)


def get_sanitized_shop_param(request):
    shop = request.query_params.get('shop')
    sanitized_shop_domain = shop_url.sanitize_shop_domain(shop)

    if not sanitized_shop_domain:
        raise ValueError("Shop must match 'example.myshopify.com'")
    return sanitized_shop_domain

def build_auth_params():
    scopes = settings.SHOPIFY_API_SCOPES.split(",")

    redirect_uri = f'http://{settings.FRONTEND_URL}/shopify-callback'
    # redirect_uri = f'https://{settings.FRONTEND_URL}/shopify-callback'

    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")

    return scopes, redirect_uri, state


def _new_session(shop_url):
    shopify_api_version = settings.SHOPIFY_API_VERSION
    shopify_api_key = settings.SHOPIFY_API_KEY
    shopify_api_secret = settings.SHOPIFY_API_SECRET

    shopify.Session.setup(api_key=shopify_api_key, secret=shopify_api_secret)
    return shopify.Session(shop_url, shopify_api_version)


def build_callback_redirect_uri(request, params):
    base = request.session.get("return_to", settings.FRONTEND_URL)
    shop = params.get('shop')
    return f"{base}?shop={shop}"
