from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)

    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'

    def __str__(self):
        return self.name
    
    
    
class Product(models.Model):
    name=models.CharField(max_length=50)
    descreption=models.TextField()
    image=models.URLField(max_length=500)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    new_price=models.IntegerField()
    status=models.CharField(max_length=20,default='Active')

    def __str__(self):
        return self.name