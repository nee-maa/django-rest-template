from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=30, null=False, blank=False)
    product_count = models.IntegerField(null=False, default=0)
    product_description = models.TextField(null=True, blank=True)
    product_code = models.CharField(unique=True, db_index=True, max_length=8, null=True)

    def __str__(self):
        return self.product_name
