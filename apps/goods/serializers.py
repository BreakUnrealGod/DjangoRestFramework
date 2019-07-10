from django.db.models import Q
from rest_framework import serializers

# 分类的序列化
from goods.models import GoodsCategory, Banner, HotSearchWords, Goods, IndexAd, GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    sub_category = CategorySerializer3(many=True)  # 序列化的嵌套关系

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer1(serializers.ModelSerializer):
    sub_category = CategorySerializer2(many=True)  #

    class Meta:
        model = GoodsCategory
        fields = '__all__'


# 首页轮播图片序列化
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


# 热搜词的序列化
class HotSearchWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsImage
        fields='__all__'


# 商品 的序列化  goods 对象  ---》 images 多张
class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer1()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'


# 商品类别广告
class IndexAdSerializer(serializers.ModelSerializer):
    goods = serializers.SerializerMethodField()

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category__id=obj.id)
                                         | Q(category__parent_category__parent_category_id=obj.id))
        serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return serializer.data

