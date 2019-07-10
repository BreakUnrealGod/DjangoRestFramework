import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet

from goods.models import Goods


class GoodsFilter(FilterSet):
    pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        result = queryset.filter(Q(category_id=value) | Q(category__parent_category__id=value)
                                 | Q(category__parent_category__parent_category_id=value))
        return result

    class Meta:
        model = Goods
        fields = ('pricemin', 'pricemax', 'is_new')
