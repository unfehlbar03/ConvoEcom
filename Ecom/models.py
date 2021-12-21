from django.db import models
from django.contrib.auth.models import User
from math import ceil
# Create your models here.
class Categories(models.Model):
    category=models.CharField(max_length=100)
    image=models.ImageField(upload_to="Ecom/categories",blank=True)
    def __str__(self):
        return self.category
    class Meta:
        verbose_name_plural = "Categories"

class Variant(models.Model):
    variant=models.CharField(max_length=100)
    def __str__(self):
        return self.variant

class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=200)
    category=models.ManyToManyField(Categories,related_name="prod_category")
    variant=models.ManyToManyField(Variant,related_name="prod_variant",default=None)
    regular_price=models.IntegerField(default=0,blank=True)
    sale_price=models.IntegerField(default=0,blank=True)
    short_description=models.TextField()
    product_detail=models.TextField()
    publish_date=models.DateField()
    image1=models.ImageField(upload_to="Ecom/images")
    image2=models.ImageField(upload_to="Ecom/images",blank=True)
    image3=models.ImageField(upload_to="Ecom/images",blank=True)
    image4=models.ImageField(upload_to="Ecom/images",blank=True)

    def __str__(self):
        return self.product_name
    @property
    def get_discount(self):
        discount=self.regular_price-self.sale_price
        percent_discount=(discount/self.regular_price)*100
        return ceil(percent_discount)

class Order(models.Model):
    customer=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    date_order=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=True)
    # transaction_id=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()             #reverseRelation
        total=sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total
    
DELIVERY_CHOICES = (

    ("UNSUCCESSFUL", "UNSUCCESSFUL"),
    ("PLACED", "PLACED"),
    ("IN-TRANSIT", "IN-TRANSIT"),
    ("AT DELIVERY CENTER", "AT DELIVERY CENTER"),
    ("OUT FOR DELIVERY", "OUT FOR DELIVERY"),
    ("DELIVERED", "DELIVERED"),
    
)

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    variant=models.ForeignKey(Variant,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    delivery_status= models.CharField(max_length = 50,choices=DELIVERY_CHOICES,default = 'UNSUCCESSFUL')
    def __str__(self):
        return str(self.order)
    @property
    def get_total(self):
        total=self.product.sale_price*self.quantity
        return total

class ShippingAddress(models.Model):
    customer=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    first_name=models.CharField(max_length=200,null=True,default="")
    last_name=models.CharField(max_length=200,null=True,default="")
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=100,null=True)
    state=models.CharField(max_length=100,null=True)
    pincode=models.CharField(max_length=50,null=True)
    phone=models.CharField(max_length=50,null=True)
    
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)

class OrderUpdates(models.Model):
    update_id=models.AutoField(primary_key=True)
    ordered_item=models.ForeignKey(OrderItem,on_delete=models.SET_NULL,blank=True,null=True)
    description=models.CharField(max_length=300)
    timeStamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ordered_item)+" "+str(self.description)

    class Meta:
        verbose_name_plural = "Order Updates"

