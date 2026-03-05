import django_filters as filters
from django.db.models import Q

from .models import User


class UserFilter(filters.FilterSet):
    # Text search (email, name, phone)
    search = filters.CharFilter(method="filter_search")

    # Choice filters
    status = filters.ChoiceFilter(choices=User.USER_STATUS_CHOICES)

    # Boolean filters
    is_active = filters.BooleanFilter()
    is_staff = filters.BooleanFilter()
    email_verified = filters.BooleanFilter()
    phone_verified = filters.BooleanFilter()

    # Date range filters
    date_joined_from = filters.DateFilter(field_name="date_joined", lookup_expr="gte")
    date_joined_to = filters.DateFilter(field_name="date_joined", lookup_expr="lte")

    class Meta:
        model = User
        fields = [
            "status",
            "is_active",
            "is_staff",
            "email_verified",
            "phone_verified",
        ]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(email__icontains=value)
            | Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(phone__icontains=value)
        )
