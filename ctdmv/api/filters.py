from django_filters.rest_framework import (
    DjangoFilterBackend, FilterSet, OrderingFilter, filters
)

from ctdmv.models import WaitEntry


class WaitEntryFilter(FilterSet):
    service = filters.CharFilter(field_name="service__name", lookup_expr="icontains")
    branch = filters.CharFilter(field_name="branch__name", lookup_expr="icontains")
    date = filters.DateFromToRangeFilter(field_name="creation_date_utc")

    class Meta:
        model = WaitEntry
        fields = ["service", "branch", "date"]
