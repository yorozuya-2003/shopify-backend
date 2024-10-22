from django.conf import settings
from django.urls import reverse

import shopify

from ..models import Shop
from .login import create_shopify_session


def validate_params(request, params):
    # validate_state_params(request, params.get("state"))

    # validate hmac
    if not shopify.Session.validate_params(params):
        raise ValueError("Invalid callback parameters")


def validate_state_params(request, state):
    # TODO: handle this
    if request.session.get("shopify_oauth_state_param") != state:
        raise ValueError("Anti-forgery state parameter does not match")

    request.session.pop("shopify_oauth_state_param", None)


def exchange_code_for_access_token(request, shop):
    session = create_shopify_session(shop)
    access_token = session.request_token(request.query_params.dict())
    access_scopes = session.access_scopes

    return access_token, access_scopes


def store_shop_information(access_token, access_scopes, shop_domain):
    shop = Shop.objects.get_or_create(domain=shop_domain)[0]
    shop.shopify_token = access_token
    shop.access_scopes = access_scopes

    shop.save()


def shopify_session(shopify_domain, access_token):
    api_version = settings.SHOPIFY_API_VERSION

    return shopify.Session.temp(shopify_domain, api_version, access_token)


def get_api_endpoint(namespace):
    api_url = settings.SHOPIFY_API_URL
    endpoint = api_url + reverse(namespace)

    return endpoint


def create_uninstall_webhook(shop, access_token):
    with shopify_session(shop, access_token):
        webhook = shopify.Webhook()
        webhook.topic = "app/uninstalled"
        webhook.address = get_api_endpoint('uninstall')
        webhook.format = "json"
        webhook.save()


def create_order_create_webhook(shop, access_token):
    with shopify_session(shop, access_token):
        webhook = shopify.Webhook()
        webhook.topic = "orders/create"
        webhook.address = get_api_endpoint('webhook_order_create')
        webhook.format = "json"
        webhook.save()