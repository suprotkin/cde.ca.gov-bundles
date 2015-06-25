""""""

from ambry.bundle.loader import LoaderBundle


class Bundle(LoaderBundle):
    @staticmethod
    def clean_stars(v):
        
        if '*' in v:
            return None
        else:
            return v
    
    def row_mangler(self, source, row_gen, row):
        """
        Override this function to alter each row of a source file, just after it is passed out of a Delimited file
        reader in the DelimitedRowGenerator
        :param row:
        :return:
        """
        # print self.schema
        # print source, row_gen, row
        # raise
        if row_gen._header and len(row_gen._header) < len(row):
            
            if '\t' in row:
                raise Exception() # tabs should be handled by filetype in the sources. 

            i =  len(row_gen._header) -1
            row = row[:i] + [','.join(row[i:])]
        return row