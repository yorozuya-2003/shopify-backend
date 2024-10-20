from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import shopify
shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)


class ProductList(APIView):
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
            products = shopify.Product.find()
            
        return Response({'products': [product.to_dict() for product in products]}, status=status.HTTP_200_OK)
    