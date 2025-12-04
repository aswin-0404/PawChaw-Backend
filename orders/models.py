from django.db import models
from products.models import Product
from accounts.models import Register

# Create your models here.
class Order(models.Model):
    payment_choice=(
        ('COD','cash on Delivery'),
        ('UPI','UPI'),
        ('CARD','Card Payment'),
        ('NET BANKING','Net Banking'),
    )

    status_choice=(
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Deliverd','Deliverd'),
        ('Cancelled','Cancelled'),
    )

    user=models.ForeignKey(Register,on_delete=models.CASCADE,related_name='orders')

    full_name=models.CharField(max_length=50)
    email=models.EmailField()
    address=models.TextField()
    city=models.CharField(max_length=50)
    zip=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)

    payment_method=models.CharField(max_length=25,choices=payment_choice,default='COD')

    status=models.CharField(max_length=25,choices=status_choice,default='Pending')

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"order {self.id}-{self.user.email}"

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField(default=1)
    price=models.IntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"