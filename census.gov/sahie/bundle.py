""""""

from ambry.bundle.loader import CsvBundle


class Bundle(CsvBundle):
    @staticmethod
    def clean_na(v):

        if 'N/A' in v:
            return None
        else:
            return v