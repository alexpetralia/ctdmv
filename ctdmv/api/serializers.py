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

    DATA_COLS = ['wait_time_mins', 'num_waiting', 'creation_date_utc']

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
        df = self.qs.to_dataframe()[self.__class__.DATA_COLS]
        dfx = df.groupby(self._get_grouped_col(df)).mean()

        # If grouping by time, slide to nearest 5-minute interval
        if hasattr(dfx.index, 'levels') and len(dfx.index.levels) > 1:
            idx = pd.Int64Index([5 * round(x / 5) for x in dfx.index.levels[1]])
            dfx.index = dfx.index.set_levels(idx, level=1)

        # Convert to JSON for datetime->str conversion, then back to JSON
        return json.loads(dfx.to_json(date_format='iso'))
