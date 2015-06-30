""""""

from ambry.bundle.loader import TsvBuildBundle
from ambry.bundle.rowgen import DelimitedRowGenerator


class Bundle(TsvBuildBundle):
    def row_gen_for_source(self, source_name, use_row_spec = True):

        fn = self.filesystem.download(source_name)

        return DelimitedRowGenerator(fn, delimiter=self.delimiter)
