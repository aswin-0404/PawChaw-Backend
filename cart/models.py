from django.db import models
from accounts.models import Register
from products.models import Product

# Create your models here.
class CartItems(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE,related_name='cartitems')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.email}-{self.product.name}x{self.quantity}"