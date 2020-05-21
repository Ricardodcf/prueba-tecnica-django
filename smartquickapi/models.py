from django.db import models


class User(models.Model):
    
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, null=False, blank=False)
    token = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "user"


class Client(models.Model):
    
    document = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)

    class Meta:
        db_table = "client"

class Product(models.Model):
    
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    class Meta:
        db_table = "product"

class Bill(models.Model):
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    nit = models.CharField(max_length=100)
    code = models.CharField(max_length=200)

    class Meta:
        db_table = "bill"

class BillProduct(models.Model):

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "bill_product"




