""""""

from ambry.bundle.loader import TsvBuildBundle
from ambry.bundle.rowgen import DelimitedRowGenerator
import csv, codecs, cStringIO


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeDelimitedRowGenerator(DelimitedRowGenerator):
    def get_csv_reader(self, f, sniff=False):
        if sniff:
            dialect = csv.Sniffer().sniff(f.read(5000))
            f.seek(0)
        else:
            dialect = None

        delimiter = self.delimiter or ','

        return UnicodeReader(f, delimiter=delimiter, dialect=dialect)


class Bundle(TsvBuildBundle):
    def row_gen_for_source(self, source_name, use_row_spec = True):

        source = self.metadata.sources[source_name]

        fn = self.filesystem.download(source_name)

        if fn.endswith('.zip'):
            sub_file = source.file
            fn = self.filesystem.unzip(fn, regex=sub_file)

        return UnicodeDelimitedRowGenerator(fn, delimiter=self.delimiter)
