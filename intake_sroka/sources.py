from . import __version__
from intake.source.base import DataSource, Schema
__all__ = ['GASource', 'AthenaSource']

# Google analytics
# Google Ad Manager - required googleads
# https://pypi.org/project/googleads/
# from sroka.api.google_ad_manager.gam_api import get_data_from_admanager
# Qubole
from sroka.api.qubole.query_result_file import get
# MOAT
from sroka.api.moat.moat_api import get_data_from_moat
# Rubicon
from sroka.api.rubicon.rubicon_api import get_data_from_rubicon


class SrokaSourceBase(DataSource):
    container = "dataframe"
    version = __version__
    partition_access = False

    def get_scheme(self):
        if self.df is None:
            self.df = self._make_df()
        dtypes = self.df.dtypes.to_dict()
        dtypes = {n: str(t) for (n, t) in dtypes.items()}
        return Schema(dtype=dtypes, shape=self.df.shape,
                      extra_metadata=self.metadata,
                      npartitions=1)


class AthenaSource(SrokaSourceBase):
    name = "athena"

    def __init__(self, query, **kwargs):
        self.query = query
        self.df = None
        super().__init__(**kwargs)

    def _make_df(self):
        from sroka.api.athena.athena_api import query_athena
        return query_athena(self.query)


class GASource(SrokaSourceBase):
    """
    API reference:
    https://developers.google.com/analytics/devguides/reporting/core/v3/reference

    Dimensions and metric sets:
    https://developers.google.com/analytics/devguides/reporting/core/dimsmets
    """
    name = 'google_analytics'

    def __init__(self, id, metrics, **kwargs):
        import pandas as pd
        q = {"ids": "ga:{}".format(id),
             "metrics": metrics}
        for val in "start_date", "end_date", "filters", "segment", "dimensions":
            if val in kwargs:
                if 'date' in val:
                    q[val] = pd.to_datetime(kwargs[val]).date().isoformat()
                else:
                    q[val] = kwargs[val]
        self.q = q
        self.sampling = kwargs.get('sampling_level', 'FASTER')

    def _make_df(self):
        from sroka.api.ga.ga import ga_request
        ga_request(self.q, sampling_level=self.sampling)


class GSheetSource(SrokaSourceBase):

    def __init__(self, sheetname_id, sheet_range, first_row_columns=False,
                 **kwargs):
        self.sheet = sheetname_id
        self.range = sheet_range
        self.first = first_row_columns
        super().__init__(**kwargs)

    def _make_df(self):
        from sroka.api.google_drive.google_drive_api import \
            google_drive_sheets_read
        return google_drive_sheets_read(self.sheet, self.range, self.first)

