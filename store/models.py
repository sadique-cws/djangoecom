from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField()

    # def get_absolute_url(self):
    #     return reverse("store:category",kwargs={
    #         'slug':self.slug
    #     })

    def __str__(self):
        return self.title

class Brand(models.Model):
    brand_name = models.CharField(max_length=200)
    slug = models.SlugField()
    #
    # def get_absolute_url(self):
    #     return  reverse("store:brand",kwargs={
    #     "slug":self.slug
    #    })

    def __str__(self):
        return self.brand_name

class Item(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    slug = models.SlugField(null=True,blank=True)
    image = models.ImageField()
    price = models.FloatField()
    discount_price = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:product",kwargs={
            "slug":self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart",kwargs={
            "slug":self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart", kwargs={
            "slug": self.slug
        })

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Item, self).save(*args,**kwargs)

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.item.title

    def get_total_price(self):
        return self.qty * self.item.price

    def get_total_discount_price(self):
        return self.qty * self.item.discount_price

    def get_total_saving_amount(self):
        return self.get_total_price() - self.get_total_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        else:
            return self.get_total_price()



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(null=True)
    add_date = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey('Coupon',on_delete=models.SET_NULL,blank=True,null=True)

    def get_total(self):
        total = 0
        for oi in self.items.all():
            total += oi.get_final_price()

        if self.coupon:
            total -= (total * self.coupon.percentage)/100
        return total

    def get_coupon_amount(self):
        total = 0
        for oi in self.items.all():
            total += oi.get_final_price()

        return (total * self.coupon.percentage) / 100

class Coupon(models.Model):
    code = models.CharField(max_length=200)
    percentage = models.IntegerField()

    def __str__(self):
        return self.code

