from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, \
    RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import ShopCartSerializer, ShopCartListSerializer, OrderInfoSerializer, OrderInfoDetailSerializer


class ShopCartViewset(ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)

    #
    # serializer_class =ShopCartSerializer  ShopCartListSerializer
    def get_serializer_class(self):
        if self.action == 'list':  # [ShopCart,ShopCart,ShopCart,ShopCart]
            return ShopCartListSerializer
        return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_object(self):
        user = self.request.user
        goodsid = self.kwargs['pk']

        shopingcart = ShoppingCart.objects.filter(user=user, goods_id=goodsid)  # queryset []
        if shopingcart:
            return shopingcart.first()
        return None


order_sn = 0


class OrderViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)

    # serializer_class = OrderInfoSerializer  OrderInfoDetailSerializer
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderInfoDetailSerializer
        return OrderInfoSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()  # 创建一笔订单
        global order_sn
        order_sn += 1
        order.order_sn = '000000' + str(order_sn)

        order.save()
        print('----->', serializer.validated_data)
        # 清空购物车
        '''
        goods_id   user_id  nums
          1         5        2   ----->shopcart
          6         5        5
          9         5        1
          [shopcart,shopcart,shopcart]
        '''
        shopcarts = ShoppingCart.objects.filter(user=self.request.user)
        for shopcart in shopcarts:
            orderGoods = OrderGoods()
            orderGoods.goods_num = shopcart.nums
            orderGoods.goods = shopcart.goods
            orderGoods.order = order
            orderGoods.save()

            # delete
            shopcart.delete()


'''
 post_script: this.post_script,  留言
              address: this.address,  收货地址
              signer_name: this.signer_name,  收货人
              singer_mobile: this.signer_mobile,  联系方式
              order_mount: this.totalPrice   总价
'''
