from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'role', RoleViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'canteen', CanteenViewSet)
router.register(r'window', WindowViewSet)
router.register(r'dish', DishViewSet)
router.register(r'dish-like', DishLikeViewSet)
router.register(r'dish-favorite', DishFavoriteViewSet)
router.register(r'dish-comment', DishCommentViewSet)
router.register(r'dish-order', DishOrderViewSet)
router.register(r'address', AddressViewSet)
router.register(r'swiper', SwiperViewSet)
router.register(r'feedback', FeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/role/', RoleSearchView.as_view()),
    path('search/profile/', ProfileSearchView.as_view()),
    path('search/canteen/', CanteenSearchView.as_view()),
    path('search/window/', WindowSearchView.as_view()),
    path('search/dish/', DishSearchView.as_view()),
    path('search/dish-like/', DishLikeSearchView.as_view()),
    path('search/dish-favorite/', DishFavoriteSearchView.as_view()),
    path('search/dish-comment/', DishCommentSearchView.as_view()),
    path('search/dish-order/', DishOrderSearchView.as_view()),
    path('dataAnalysis/dish/', Dish_DataAnalysisView.as_view()),
    path('search/address/', AddressSearchView.as_view()),
    path('search/swiper/', SwiperSearchView.as_view()),
    path('search/feedback/', FeedbackSearchView.as_view()),

    # 模拟支付接口--支付宝沙箱
    path("payment/", alipay_pay, name="alipay_pay"),
    path("payment/notify/", alipay_notify, name="alipay_notify"),

    path('check-username/', CheckUsernameView.as_view(), name='check-username'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('setting-password/', SettingPasswordView.as_view(), name='setting-password'),
    path('dish-comment-frontend/', DishCommentFrontendViewSet.as_view({"get":"list"}), name='dish-comment-frontend')
]
