from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ..models import Order
from ..utils import webhook


class OrderCreateWebhook(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        if not webhook.validate_webhook(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            webhook_data = request.data

            with transaction.atomic():
                order = Order(
                    order_id=webhook_data['id'],
                    contact_email=webhook_data['contact_email'],
                    created_at=webhook_data['created_at'],
                    currency=webhook_data['currency'],
                    current_subtotal_price=webhook_data['current_subtotal_price'],
                )
                order.save()
        
                return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
