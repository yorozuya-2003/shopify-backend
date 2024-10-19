from django.conf import settings

from ..models import Shop
from .login import _new_session

import shopify


def validate_params(request, params):
    # validate_state_param(request, params.get("state"))

    # validate hmac
    if not shopify.Session.validate_params(params):
        raise ValueError("Invalid callback parameters")


def validate_state_param(request, state):
    # TODO: handle this
    if request.session.get("shopify_oauth_state_param") != state:
        raise ValueError("Anti-forgery state parameter does not match")

    request.session.pop("shopify_oauth_state_param", None)


def exchange_code_for_access_token(request, shop):
    session = _new_session(shop)
    access_token = session.request_token(request.query_params.dict())
    access_scopes = session.access_scopes

    return access_token, access_scopes


def store_shop_information(access_token, access_scopes, shop):
    shop_record = Shop.objects.get_or_create(shopify_domain=shop)[0]
    shop_record.shopify_token = access_token
    shop_record.access_scopes = access_scopes

    shop_record.save()


def shopify_session(shopify_domain, access_token):
    api_version = settings.SHOPIFY_API_VERSION

    return shopify.Session.temp(shopify_domain, api_version, access_token)


def create_uninstall_webhook(shop, access_token):
    with shopify_session(shop, access_token):
        app_url = settings.SHOPIFY_APP_URL
        webhook = shopify.Webhook()
        webhook.topic = "app/uninstalled"
        webhook.address = f"https://{app_url}/api/uninstall/"
        webhook.format = "json"
        webhook.save()
