from django.db.models import fields
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework_simplejwt.tokens import Token
from .models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.serializers import ModelSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields =['email', 'password']

    def validate(self, attrs):

        email=attrs.get('email','')
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({'email is already used'})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password= serializers.CharField(max_length=68, min_length=6,write_only=True)
    tokens=serializers.CharField(max_length=68, min_length=6,read_only=True)
    tokenRe=serializers.CharField(max_length=68, min_length=6,read_only=True)
    id = serializers.CharField(max_length=68, min_length=1,read_only=True)
    class Meta:
        model=User
        fields=['email','password','tokens','tokenRe',"id"]
    def validate(self, attrs):
        email=attrs.get('email','')
        password=attrs.get('password','')

        user=auth.authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed('Ivalid credential, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disable, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Account has not verified yet, check register mail again')
        
        return {
            'id': user.id,
            'email':user.email,
            'tokens':user.tokens,
            'tokenRe': user.tokenRe
        }
class ResetPasswordViaEmailSerializer(serializers.Serializer):
    email=serializers.EmailField( min_length=2)

    class Meta:
        fields=['email']
    
class ResetPassWordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=68, min_length=6,write_only=True)
    token=serializers.CharField( min_length=1,write_only=True)
    uidb64=serializers.CharField( min_length=1,write_only=True)

    class Meta:
        fields=['password','token','uidb64']
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return(user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields=['id','name', 'email', "phone","orders", "avt", "sex", "dateofbirth"]
        extra_kwargs ={
            'password' :{'write_only':'true'}
        }
class UploadAvtSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','avt']
        
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description","price", "sold", "quantity","instruction", "origin","IsActive", "images", "category","priceSale","IsFlashsale"]
    extra_kwargs ={
            'sold' :{'write_only':'true'}
        }

class ProductTypeSerializer(ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["id", "name"]


class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields=["id", "name","imagecategory", "producttype"]

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model=ProductImage
        fields=["id","img"] 

class RatingSerializer(ModelSerializer):
    class Meta:
        model=Rating
        fields=["id","dayandtime","ratingpoint", "ratingcomment","img","product","user"] 
class LoveListSerializer(ModelSerializer):
    class Meta:
        model= LoveList
        fields= '__all__'

class TagSerializer(ModelSerializer):
    class Meta:
        model= IngredientsTag
        fields= '__all__'

class IngredientSerializer(ModelSerializer):
    class Meta:
        model= Ingredients
        fields= ["id","name","Tag","Description","levelOfSave"]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
    def create(self, validated_data):
        return super().create(validated_data)

class ProvinceSerializer (ModelSerializer):
    class Meta:
        model = Provinces
        fields = '__all__'

class DistrictSerializer(ModelSerializer):
    class Meta:
        model = Districts
        fields = '__all__'

class WardSerializer(ModelSerializer):
    class Meta:
        model = Wards
        fields = '__all__'
class DeliverySerializer(ModelSerializer):
    class Meta:
        model= Delivery
        fields = '__all__'
class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
class DetailOrderSerializer(ModelSerializer):
    class Meta:
        model = DetailOrder
        fields = '__all__'

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'