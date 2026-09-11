from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    price = models.IntegerField()
    image = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    stock = models.IntegerField(default=10)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Order(models.Model):
    user_name = models.CharField(max_length=100)
    items = models.CharField(max_length=500)
    total = models.IntegerField()
    status = models.CharField(max_length=50, default="Pending")
    payment_status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Order {self.id}"
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items"
    )
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=200)
    product_price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=20)
    product_image = models.CharField(max_length=300)

    def __str__(self):
        return self.product_name
class Review(models.Model):
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"