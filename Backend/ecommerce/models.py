from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,PermissionsMixin)
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL 
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.utils.text import slugify
# Create your models here.
# add table product type chỉnh PK, thêm trường product
class UserManager(BaseUserManager):
    def create_user(self, email,password=None):
        if email is None:
            raise TypeError('Users should have an email')
        user= self.model( email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,password=None):
        if password is None:
            raise TypeError('Password should not None')
        user= self.create_user( email,password)
        user.is_superuser=True
        user.is_Staff=True
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified= models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    avt = models.ImageField(upload_to='avt',default='logo-uit.png')
    name = models.CharField(max_length=60,null=True,blank=True)
    phone = models.CharField(max_length=10, null=True,blank=True)
    sex = models.CharField(max_length=10,null=True,blank=True)
    orders = models.IntegerField(null=True,blank=True, default=0)
    dateofbirth=models.DateField(null=True, blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    objects = UserManager()

    def __str__(self):
        return self.email
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)
            #'refresh':str(refresh),
            #'access':
    def tokenRe(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh)       
        

User._meta.get_field('email')._unique = True
User._meta.get_field('email')._blank = False


class ProductImage(models.Model):
    img=models.ImageField(upload_to='media',default=None)
    

class ProductCategory(models.Model):
    name = models.CharField(max_length=300,null=True, blank=True)
    imagecategory = models.ImageField(upload_to='media',default=None)
    producttype = models.ForeignKey("ProductType", on_delete=SET_NULL, null=True)
    def __str__(self):
        return self.name

class ProductType(models.Model):
    name = models.CharField(max_length=300,null=True, blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=500, null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    sold = models.IntegerField(default=0,null=True, blank=True)
    quantity = models.IntegerField(default=0,null=True, blank=True)
    instruction =models.TextField(null=True, blank=True)
    origin=models.CharField(max_length=50,null=True, blank=True)
    IsActive= models.BooleanField(default=True)
    images=models.ManyToManyField("ProductImage",blank=True,)
    category=models.ForeignKey(ProductCategory,on_delete=models.SET_NULL,null=True)
    IsFlashsale= models.BooleanField(default=False)
    priceSale = models.IntegerField(null=True,blank=True)
    # add pricesale, isSale: already
    
class Rating(models.Model):
    dayandtime = models.DateTimeField(auto_now_add=True)
    ratingpoint = models.IntegerField(null=True,blank=True)
    ratingcomment = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='static',default=None)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class LoveList(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)

class IngredientsTag(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class Ingredients(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    levelOfSave = models.IntegerField(null=True, blank=True)
    Description = models.TextField(null=True,blank=True)
    Tag = models.ManyToManyField("IngredientsTag", blank=True, )
    slug = models.SlugField(null=True, blank=True,)
    
    def __str__(self):
        return self.name 

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug=slugify(self.name)
        super().save(*args, **kwargs)

class Provinces (models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)

class Districts (models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    province = models.ForeignKey(Provinces,on_delete=models.SET_NULL,null=True)

class Wards (models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    district = models.ForeignKey(Districts,on_delete=models.SET_NULL,null=True)

class Delivery(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    province =  models.ForeignKey(Provinces,on_delete=models.SET_NULL,null=True)
    district = models.ForeignKey(Districts,on_delete=models.SET_NULL,null=True)
    ward = models.ForeignKey(Wards,on_delete=models.SET_NULL,null=True)
    address = models.TextField(null=True,blank=True)
    fullAddress = models.TextField(null=True,blank=True)
    defaultAddress = models.TextField(null=True,blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    receiveName = models.CharField(max_length=50, null=True, blank=True)
    receiveGender = models.CharField(max_length=10, null=True, blank=True)

class Order (models.Model):
    dateCreate = models.DateField(auto_now_add=True)
    dateReceive = models.DateField(null=True, blank=True)
    totalValue = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=70, null=True, blank=True)
    cancellationReason = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    delivery = models.ForeignKey(Delivery,on_delete=models.SET_NULL,null=True)

class DetailOrder (models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantities = models.IntegerField(null=True, blank=True)

class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    isSelections = models.BooleanField(default=False)
    quantities =  models.IntegerField(null=True, blank=True)