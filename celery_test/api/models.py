import uuid

from django.contrib.auth.models import User
from django.db import models


ORDER_CHOICES = ((3, 'delivered'), (-1, 'canceled'), (0, 'pending'), (1, 'ready to send'), (2, 'sent'))


class Product(models.Model):
    product_name = models.CharField(max_length=30, null=False, blank=False)
    product_count = models.IntegerField(null=False, default=0)
    product_description = models.TextField(null=True, blank=True)
    product_code = models.CharField(unique=True, db_index=True, max_length=8, null=True)
    rate = models.SmallIntegerField()

    def __str__(self):
        return self.product_name


class Costumer(models.Model):
    profile = models.ForeignKey('Profile', related_name='costumer', on_delete=models.SET_NULL, null=True)
    costumer_id = models.UUIDField(default=uuid.uuid4())


class Owner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey('Profile', related_name='owner', on_delete=models.SET_NULL, null=True)
    costumer_id = models.UUIDField(default=uuid.uuid4())
    rate = models.SmallIntegerField()


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=13)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    avatar = models.ImageField(null=True)


class Orders(models.Model):
    costumer_id = models.ForeignKey(Costumer, on_delete=models.SET_NULL, null=True)
    state = models.IntegerField(choices=ORDER_CHOICES)
