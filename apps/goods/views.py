import django_filters
from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from goods.filter import GoodsFilter
from goods.models import GoodsCategory, Banner, HotSearchWords, Goods
from goods.serializers import CategorySerializer1, BannerSerializer, HotSearchWordSerializer, IndexAdSerializer, \
    GoodsSerializer


class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer1


class BannerViewSet(ListModelMixin, GenericViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


# 热搜词
class HotSearchWordViewSet(ListModelMixin, GenericViewSet):
    queryset = HotSearchWords.objects.all()
    serializer_class = HotSearchWordSerializer


# 商品类别广告
class IndexAdViewSet(ListModelMixin, GenericViewSet):
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['', ''])
    serializer_class = IndexAdSerializer


# 分页的定制类
class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'  # http://api.example.org/accounts/?page=4&page_size=100
    max_page_size = 100
    page_size_query_param = 'page_size'


class GoodsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter)  # 默认后端
    # filterset_fields= ('name','is_new')
    filter_class = GoodsFilter  # 自定义

    search_fields = ('name', 'goods_brief', 'goods_desc')

    # 排序筛选
    ordering_fields = ('sold_num', 'shop_price')
    # 当前类视图使用的分页器类
    pagination_class = GoodsPagination

    # 添加局部的认证
    # authentication_classes = (BasicAuthentication, SessionAuthentication, TokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     result = self.request.GET.get('is_new', None)
    #     print('------>', result)
    #     print('------->kwargs:', self.kwargs)
    #     if result:
    #         return Goods.objects.filter(is_new=result).order_by('-add_time')[:5]
    #     return Goods.objects.all()
