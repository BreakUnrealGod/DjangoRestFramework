from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from goods.models import Goods
from goods.serializers import GoodsSerializer
from trade.models import ShoppingCart, OrderInfo, OrderGoods


#   1  images  3


#  1  shijian  1   1  8  --->ShopCart object   ----   goods
#  2  shijian  3   1  2
#  3 shijian   9   1  1

# list_cart = [ShopCart,ShopCart,ShopCart,ShopCart]   --->
class ShopCartListSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('goods', 'nums')


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())
    nums = serializers.IntegerField(required=True, min_value=1, error_messages={
        'required': '商品数量必须添加',
        'min_value': '商品数量不能少于1'
    })

    def create(self, validated_data):
        # goods: this.productId, // 商品id   nums: this.buyNum, // 购买数量
        goods = validated_data['goods']
        nums = validated_data['nums']
        user = self.context['request'].user

        # 进行数据库的查询
        shopcart = ShoppingCart.objects.filter(user=user, goods=goods)
        if shopcart.exists():
            # 原来在购物车中存在此商品
            cart = shopcart.first()
            cart.nums += nums
            cart.save()
        else:
            # 购物车中此用户没有添加过此商品
            cart = ShoppingCart.objects.create(user=user, goods=goods, nums=nums)
        return cart

    def update(self, instance, validated_data):
        # instance shopcart对象
        instance.nums = validated_data['nums']
        instance.save()
        return instance


# 订单详情
class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)   # 一个订单商品中就包含一条商品

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderInfoDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)  # 一笔订单可以有多件商品

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    # order_sn = serializers.IntegerField(read_only=True)
    # trade_no = serializers.IntegerField(read_only=True)
    # pay_status = serializers.CharField(read_only=True)
    # pay_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'
