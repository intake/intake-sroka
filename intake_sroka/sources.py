from intake.source import base
from . import __version__

__all__ = ['GASource']


class GASource(base.DataSource):
    """
    """
    container = 'dataframe'
    name = 'google_analytics'
    version = __version__
    partition_access = True

    def __init__(self, query):
        pass
