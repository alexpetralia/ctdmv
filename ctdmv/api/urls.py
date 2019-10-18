from django.urls import path, include
from rest_framework.routers import SimpleRouter

from ctdmv.api import viewsets


class OptionalSlashRouter(SimpleRouter):
    def __init__(self):
        self.trailing_slash = "/?"
        super(SimpleRouter, self).__init__()


router = OptionalSlashRouter()
router.register('wait_times', viewsets.WaitEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
