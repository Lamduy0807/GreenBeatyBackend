from django.urls import path
from .views import *
from django.urls.conf import include
from django.contrib.auth import views as auth_view
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)
from .import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
router = DefaultRouter()

router.register('product', views.ProductViewSet)
router.register('category',views.CategoryViewSet)
router.register('type',views.ProductTypeViewSet)
router.register('img',views.ProductImageViewSet)
#router.register('rating', views.RatingViewSet)
router.register("lovelist",views.LoveListViewSet)
router.register("tag",views.TagViewSet)
router.register("ingredient",views.IngredientsViewSet)
router.register("user", views.UserViewSet)
router.register("delivery", views.DeliveryViewSet)
router.register("provinces", views.ProvinceViewSet)
router.register("districts", views.DistrictViewSet)
router.register("wards", views.WardViewSet)
router.register("order", views.OrderViewSet)
router.register("detailorder", views.DetailOrderViewSet)
router.register("cart", views.CartViewSet)
router.register("banner", views.BannerViewSet)
urlpatterns=[
    path('',include(router.urls)),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('request-reset-email/',RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('rating/<user>/',RatingViewSet1.as_view(),name = "getuser"),
    path('rating/<id>/<point>/',RatingViewSet.as_view(),name = "rating-point"),
    path('password-reset/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name="ecommerce/reset_form.html"),name='password-reset'),
    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name="ecommerce/reset_done.html"),name='password_reset_complete'),
    path('test/<id>/', RecommendViewSet.as_view()),
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)