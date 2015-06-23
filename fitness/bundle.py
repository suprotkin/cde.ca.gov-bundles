""""""

from ambry.bundle.loader import TsvBuildBundle
from ambry.bundle.rowgen import DelimitedRowGenerator


class Bundle(TsvBuildBundle):

    def row_gen_for_source(self, source_name, use_row_spec = True):

        source = self.metadata.sources[source_name]

        fn = self.filesystem.download(source_name)

        delimiter = getattr(source, 'filetype', 'csv') == 'csv' and ',' or '\t'

        if fn.endswith('.zip'):
            sub_file = source.file
            fn = self.filesystem.unzip(fn, regex=sub_file)

        return DelimitedRowGenerator(fn, delimiter=delimiter, encoding=getattr(source, 'encoding', 'utf-8'))
