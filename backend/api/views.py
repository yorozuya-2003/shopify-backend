from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Shop
from .utils import login, callback

import shopify
shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)


class Login(APIView):
    def get(self, request):
        shop = request.query_params.get('shop')
        if shop:
            return login.authenticate(request)
        return Response({"error": "Shop domain required"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        return login.authenticate(request)


class Callback(APIView):
    def get(self, request):
        params = request.query_params
        shop = params.get("shop")

        try:
            callback.validate_params(request, params)
            access_token, access_scopes = callback.exchange_code_for_access_token(request, shop)
            callback.store_shop_information(access_token, access_scopes, shop)
            callback.create_uninstall_webhook(shop, access_token)
            
        except ValueError as exception:
            return Response({"error": str(exception)}, status=status.HTTP_400_BAD_REQUEST)

        redirect_uri = login.build_callback_redirect_uri(request, params)
        return Response({
            "success": True,
            "redirect_uri": redirect_uri,
            "accessToken": access_token,
            "shop": shop}, status=status.HTTP_200_OK)

class Uninstall(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        uninstall_data = request.data
        shop = uninstall_data.get("domain")
        
        Shop.objects.filter(shopify_domain=shop).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


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
    