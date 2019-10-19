from django.urls import path, include
from rest_framework.routers import SimpleRouter

from ctdmv.api import viewsets


class OptionalSlashRouter(SimpleRouter):
    def __init__(self):
        self.trailing_slash = "/?"
        super(SimpleRouter, self).__init__()


router = OptionalSlashRouter()
router.register('wait_times', viewsets.WaitEntryViewSet)
router.register('branches', viewsets.BranchViewSet)
router.register('services', viewsets.ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
