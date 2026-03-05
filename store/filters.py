import django_filters as filters
from django.db.models import Q
from .models import Store


class StoreFilter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")
    owner = filters.NumberFilter()
    status = filters.ChoiceFilter(choices=Store.STATUS_CHOICES)
    phone_verified = filters.BooleanFilter()
    email_verified = filters.BooleanFilter()

    date_joined_from = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_joined_to = filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Store
        fields = ["verified", "owner", "phone_verified", "email_verified"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(slug__icontains=value)
            | Q(description__icontains=value)
            | Q(email__icontains=value)
            | Q(phone__icontains=value)
            | Q(website__icontains=value)
            | Q(address__icontains=value)
            | Q(facebook__icontains=value)
            | Q(instagram__icontains=value)
            | Q(twitter__icontains=value)
            | Q(seo_title__icontains=value)
            | Q(seo_description__icontains=value)
        )
