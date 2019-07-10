from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsSerializer
from user_operation.models import UserAddress, UserLeavingMessage, UserFav


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserAddress
        exclude = ['add_time', ]


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserLeavingMessage
        exclude = ['add_time', ]


# 用户收藏序列化
class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserFav
        fields = ('id', 'user', 'goods')
        validators = [
            UniqueTogetherValidator(queryset=UserFav.objects.all(), fields=('user', 'goods'), message='商品已收藏')
        ]


#  http://127.0.0.1:8000/userfavs/1/

class UserFavGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('id', 'goods')
