from django.db import models
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.
class Category(models.Model):
    cate_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.cate_name


class Product(models.Model):
    cate = models.ForeignKey(Category, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    img = models.ImageField()
    slug = models.SlugField()

    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse("cf:product", kwargs={
            'slug' : self.slug
        })
    
    def get_add_cart_url(self):
        return reverse("cf:add-cart", kwargs={
            'slug' : self.slug
        })
    
    def get_remove_cart_url(self):
        return reverse("cf:remove-cart", kwargs={
            'slug' : self.slug
        })    


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} {self.product.name}"


    def get_total_product_price(self):
        return (self.quantity)*(self.product.price)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return (self.user.username)

    def total_price(self):
        total = 0
        for item in self.products.all():
            total = total + item.get_total_product_price()
        return total