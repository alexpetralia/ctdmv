from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ctdmv.models import WaitEntry
from ctdmv.api.serializers import (
    WaitEntrySerializer, AggWaitEntrySerializer
)
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

    @action(detail=False, url_path=r'(?P<freq>[a-z]+)')
    def aggregate(self, request, pk=None, **kwargs):
        # Operate on filtered QuerySet
        qs = self.filter_queryset(self.queryset)

        if not qs:
            return Response()

        # Return default QS if `freq` is invalid
        if self.kwargs.get('freq', '') not in ('daily', 'weekly', 'monthly'):
            return Response(self.get_serializer(qs).data)

        freq = self.kwargs['freq']
        return Response(AggWaitEntrySerializer(qs, freq).data)
