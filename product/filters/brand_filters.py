import django_filters as filters
from django.db.models import Q

from product.models.brand import Brand


class BrandFilter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")

    class Meta:
        model = Brand
        fields = ["name", "slug"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(slug__icontains=value))
