from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ..utils import webhook


class ComplianceWebhook(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        if not webhook.validate_webhook(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK)
