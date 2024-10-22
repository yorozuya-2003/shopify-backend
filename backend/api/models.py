from django.db import models

class Shop(models.Model):
    domain = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    access_scopes = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.domain}'


class Order(models.Model):
    order_id = models.BigIntegerField(unique=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    currency = models.CharField(max_length=3)
    current_subtotal_price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"order {self.order_id}"
