from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.conf import settings
from django.db import connection, transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import shopify

from ..models import Order
from ..utils import webhook, db


class OrderCreateWebhook(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        if not webhook.validate_webhook(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            webhook_data = request.data
            shop_domain = request.META['HTTP_X_SHOPIFY_SHOP_DOMAIN']

            with transaction.atomic():
                order = Order(
                    order_id=webhook_data['id'],
                    shop_domain=shop_domain,
                    created_at=webhook_data['created_at'],
                    currency=webhook_data['currency'],
                    current_subtotal_price=webhook_data['current_subtotal_price'],
                )
                order.save()
        
                return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
    def get(self, request):
        api_version = settings.SHOPIFY_API_VERSION

        try:
            shop_domain = request.query_params['shopId']
        except:
            return Response({"error": "shop id parameter missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            access_token = request.META['HTTP_X_SHOPIFY_ACCESS_TOKEN']
        except:
            return Response({"error": "access token header missing"}, status=status.HTTP_400_BAD_REQUEST)

        with shopify.Session.temp(shop_domain, api_version, access_token):
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute('''
                        SELECT * FROM api_order
                        WHERE shop_domain = %s
                    ''', [shop_domain])
                
                    results = db.dictfetchall(cursor)

        return Response({'orders': results}, status=status.HTTP_200_OK)
