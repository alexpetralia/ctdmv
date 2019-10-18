from rest_framework import serializers

from ctdmv.models import WaitEntry


class WaitEntrySerializer(serializers.ModelSerializer):
    branch = serializers.CharField(source='branch.name')
    service = serializers.CharField(source='service.name')

    class Meta:
        model = WaitEntry
        fields = (
            'id', 'branch', 'service', 'wait_time_mins', 'creation_date_utc'
        )
