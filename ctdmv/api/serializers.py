import json
import pandas as pd

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


class AggWaitEntrySerializer(object):
    """Custom serializer for returning a single aggregated response"""

    DATA_COLS = ['wait_time_mins', 'num_waiting']

    def __init__(self, qs, freq):
        self.qs = qs
        self.freq = freq

    def _get_grouped_col(self, df):
        if self.freq == 'weekly':
            return df['creation_date_utc'].dt.weekday
        elif self.freq == 'monthly':
            return df['creation_date_utc'].dt.day
        elif self.freq == 'daily':
            return [
                df['creation_date_utc'].dt.hour,
                df['creation_date_utc'].dt.minute
            ]

    @property
    def data(self):
        """Returns aggregated dataset based on frequency"""
        df = self.qs.to_dataframe()

        # Localize timezone from UTC
        idx = pd.DatetimeIndex(df['creation_date_utc']).tz_convert('US/Eastern')
        df = df.set_index(idx).drop(columns='creation_date_utc').reset_index()

        # Resample to 5 minutes, then take average over a time slice
        dfx = df.groupby([
            pd.Grouper(key='creation_date_utc', freq='5T'), 'branch', 'service'
        ]).last().reset_index()
        dfy = df.groupby(self._get_grouped_col(dfx)).mean()
        dfz = dfy[self.__class__.DATA_COLS]

        # Convert to str(JSON) for datetime->str conversion, then back to JSON
        return json.loads(dfz.to_json(date_format='iso'))
