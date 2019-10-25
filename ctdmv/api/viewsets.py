from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ctdmv.models import WaitEntry, Service, Branch
from ctdmv.api.serializers import (
    WaitEntrySerializer, AggWaitEntrySerializer,
    ServiceSerializer, BranchSerializer
)
from ctdmv.api.filters import WaitEntryFilter
from ctdmv.api.pagination import StandardResultsSetPagination
from ctdmv.api.renderers import CSVFileMixin


class WaitEntryViewSet(CSVFileMixin, viewsets.ModelViewSet):
    """ViewSet for all wait entries"""

    queryset = WaitEntry.objects.all()
    serializer_class = WaitEntrySerializer
    filterset_class = WaitEntryFilter
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, )
    http_method_names = ["get"]

    FREQUENCIES = ('daily', 'weekly', 'monthly')

    @action(detail=False, url_path=r'(?P<freq>[a-z]+)')
    def aggregate(self, request, pk=None, **kwargs):
        """Return aggregated responses"""
        # Operate on filtered QuerySet
        qs = self.filter_queryset(self.get_queryset())

        if not qs or self.kwargs.get('freq', '') not in self.FREQUENCIES:
            return Response()

        freq = self.kwargs['freq']
        return Response(AggWaitEntrySerializer(qs, freq).data)


class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for all services"""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class BranchViewSet(viewsets.ModelViewSet):
    """ViewSet for all branches"""

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
