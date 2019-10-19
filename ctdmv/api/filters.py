from django_filters.rest_framework import (
    DjangoFilterBackend, FilterSet, OrderingFilter, filters
)

from ctdmv.models import WaitEntry


class WaitEntryFilter(FilterSet):
    service = filters.CharFilter(field_name="service__name", lookup_expr="icontains")
    branch = filters.CharFilter(field_name="branch__name", lookup_expr="icontains")
    date = filters.DateFromToRangeFilter(field_name="creation_date_utc")
    weekday = filters.NumberFilter(method="weekday_filter")

    class Meta:
        model = WaitEntry
        fields = ["service", "branch", "date", "weekday"]

    def weekday_filter(self, queryset, name, value):
        """
        Filters QuerySet by day of week (int). Add 2 to convert to ISO weekday
        """
        return queryset.filter(creation_date_utc__week_day=value + 2)
