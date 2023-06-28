from django.db import models
from appStore.models import Variation,products
from accounts.models import account

# Create your models here.
import uuid

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, editable=False)
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(account, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.cart_id:
            self.cart_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product