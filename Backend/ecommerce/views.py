from django.db.models import query
from django.shortcuts import render
from rest_framework import exceptions, generics, serializers
from rest_framework import permissions
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import *
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.
class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class=RegisterSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user= User.objects.get(email=user_data['email'])
        token=RefreshToken.for_user(user).access_token

        current_site=get_current_site(request).domain
        realtivelink = reverse('email-verify')
        
        absurl='http://'+current_site+realtivelink+"?token="+ str(token)
        email_body='Hi '+ user.email+ ' Use link below to verify your email \n' + absurl
        data={'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email'}
        Util.send_email(data)
        return Response(user_data,status= status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    def get(self,request):
        token= request.GET.get('token')
        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
            user=User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email':'Successfully activated'},status= status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as indentifier:
            return Response({'email':'Activation expired'},status= status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as indentifier:
            return Response({'email':'Invalid token'},status= status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializers
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK )

class RequestPasswordResetEmail(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class=ResetPasswordViaEmailSerializer
    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id) )
            token = PasswordResetTokenGenerator().make_token(user)

            current_site=get_current_site(request=request).domain
            realtivelink = reverse('password-reset',kwargs={'uidb64':uidb64,'token':token})
                
            absurl='http://'+current_site+realtivelink
            email_body='Hi, \nUse link below to reset your password \n' + absurl
            data={'email_body':email_body,'to_email':user.email,'email_subject':'Reset your password'}
            Util.send_email(data)
        return Response({'successfully':'check your email to reset your password'},status=status.HTTP_200_OK)

class PasswordTokenCheckAPIView(generics.GenericAPIView):
    def get(self, request, uidb64,token):
        try:
            id= smart_str(urlsafe_base64_decode(uidb64))
            user= User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error':'token is not valid, please check the new one'},status=status.HTTP_401_UNAUTHORIZED)
            return Response({'sucess':True, 'message':'Credential Valid','uidb64':uidb64, 'token':token},status=status.HTTP_200_OK)


        except DjangoUnicodeDecodeError as indentifier:
            return Response({'error':'token is not valid, please check the new one'},status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class=ResetPassWordSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response({'sucess':True, 'message':'Password is reset successfully'},status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    permission_classes  = [IsAuthenticated,]
class UploadViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UploadAvtSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(IsActive=True)
    serializer_class = ProductSerializer
    def get_permissions(self):
        if self.action == 'add-rating':
            return [permissions.IsAuthenticated(),]
        return [permissions.AllowAny(),]

    @action(methods=['post'], detail=True, url_path='add-rating')
    def add_Rating(self, request, pk):
        ratingcomment = request.data.get('comment')
        ratingpoint = request.data.get('point')
        img = request.data.get('img')

        if ratingcomment:
            r = Rating.objects.create(ratingcomment=ratingcomment, product = self.get_object(), ratingpoint= ratingpoint, img = img, user = request.user)
            return Response(RatingSerializer(r).data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class RatingViewSet(generics.GenericAPIView):
    queryset = Rating.objects.all()

    def get(self, request, id, point):
        if(int(point) > 0):
            r = Rating.objects.filter(product = id, ratingpoint = point)
            seri = RatingSerializer(r,many=True)
            return Response(seri.data, status=status.HTTP_200_OK)
        else:
            r = Rating.objects.filter(product = id)
            seri = RatingSerializer(r,many=True)
            return Response(seri.data, status=status.HTTP_200_OK)

class LoveListViewSet(viewsets.ModelViewSet):
    queryset = LoveList.objects.all()
    serializer_class = LoveListSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = IngredientsTag.objects.all()
    serializer_class = TagSerializer

class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'slug'

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Provinces.objects.all()
    serializer_class = ProvinceSerializer

class DistrictViewSet (viewsets.ModelViewSet):
    queryset = Districts.objects.all()
    serializer_class = DistrictSerializer

class WardViewSet(viewsets.ModelViewSet):
    queryset = Wards.objects.all()
    serializer_class = WardSerializer

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class DetailOrderViewSet(viewsets.ModelViewSet):
    queryset = DetailOrder.objects.all()
    serializer_class = DetailOrderSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer