"""OnlineShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from OnlineShop.settings import MEDIA_ROOT
from goods.views import CategoryViewSet, BannerViewSet, HotSearchWordViewSet, IndexAdViewSet, GoodsViewSet
from trade.views import ShopCartViewset, OrderViewSet
from user_operation.views import UserAddressViewSet, UserLeavingMessageViewSet, UserFavViewSet
from users.views import SmsViewSet, UserViewSet

router = DefaultRouter()
# 注册分类
router.register(r'categorys', CategoryViewSet, base_name='categorys')
router.register(r'banners', BannerViewSet, base_name='banners')
router.register(r'hotsearchs', HotSearchWordViewSet, base_name='hotsearchs')
router.register(r'indexcategorys', IndexAdViewSet, base_name='indexcategorys')
router.register(r'goods', GoodsViewSet, base_name='goods')
# 用户
router.register(r'code', SmsViewSet, base_name='code')
router.register(r'users', UserViewSet, base_name='users')

# 用户操作
router.register(r'address',UserAddressViewSet,base_name='address')
router.register(r'messages',UserLeavingMessageViewSet,base_name='messages')
router.register(r'userfavs', UserFavViewSet ,base_name='userfavs')

# 购物车
router.register(r'shopcarts',ShopCartViewset,base_name='shopcarts')
# 订单
router.register(r'orders',OrderViewSet,base_name='orders')
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^ueditor/', include('DjangoUeditor.urls')),
    path('', include(router.urls)),
    #re_path(r'^api-token-auth/', views.obtain_auth_token),  # token字符串  TokenAuthenticate
    re_path(r'login/',obtain_jwt_token)  # from rest_framework_jwt.views import obtain_jwt_token
]
