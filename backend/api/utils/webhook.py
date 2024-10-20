from django.conf import settings

import hashlib, base64, hmac


def validate_hmac(body, secret, hmac_to_verify):
    hash = hmac.new(secret.encode('utf-8'), body, hashlib.sha256)
    hmac_calculated = base64.b64encode(hash.digest()).decode('utf-8')
    return hmac_calculated == hmac_to_verify


def validate_webhook(request):
    try:
        webhook_topic = request.META['HTTP_X_SHOPIFY_TOPIC']
        webhook_hmac = request.META['HTTP_X_SHOPIFY_HMAC_SHA256']
        webhook_data = request.body
    except:
        return False

    return validate_hmac(webhook_data, settings.SHOPIFY_WEBHOOK_SIGNED_KEY, webhook_hmac)
