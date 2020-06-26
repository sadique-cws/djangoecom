from django.db import models
from django.conf import settings
from django.shortcuts import reverse

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
    slug = models.SlugField()
    image = models.ImageField()
    price = models.FloatField()
    discount_price = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("store:product",kwargs={
    #         "slug":self.slug
    #     })

