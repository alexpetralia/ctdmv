from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from ctdmv.models import WaitEntry
from ctdmv.api.serializers import WaitEntrySerializer
from ctdmv.api.filters import WaitEntryFilter
from ctdmv.api.pagination import StandardResultsSetPagination


class WaitEntryViewSet(viewsets.ModelViewSet):
    """ViewSet for all wait entries"""

    queryset = WaitEntry.objects.all()
    serializer_class = WaitEntrySerializer
    filterset_class = WaitEntryFilter
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, )
    http_method_names = ["get"]
