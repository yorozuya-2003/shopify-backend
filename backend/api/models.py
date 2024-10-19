from django.db import models

class Shop(models.Model):
    shopify_domain = models.CharField(max_length=255)
    shopify_token = models.CharField(max_length=255)
    access_scopes = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'id: {self.pk}, shop: {self.shopify_domain}, token: {self.shopify_token}, access_scopes: {self.access_scopes}'
