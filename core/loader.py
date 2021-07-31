from pathlib import Path
import glob
from collections import namedtuple

from glossary.glossarychecker import GlossaryChecker
from qa.length_checker import check_length
from qa.filter import rfilter
from core.writer import write


CheckResult = namedtuple('CheckResult', ['name', 'results'])


class Loader:
    """ Main loader to enable handling of multiple files.

    Loader class accepts single file or a folder of multiple sdlxliffs and returns a list.
    Operations such as filter or glossary checks then can be performed on all the sdlxliffs
    using for loop.

    Parameters
    ----------
    sdlxliffs : str
        str of file or directory.
    glossary : str
        str of file or directory
    ignore_list : str
        str of ignore_list with words separated by a comma.
    writer : str
        "excel" to save to an excel file.

    Methods
    -------
    glossary_check()


    check_length()


    """

    def __init__(self, sdlxliffs, glossary=None, ignore_list=None, writer="screen"):
        self._sdlxliffs = self._load(sdlxliffs)
        self._glossary = glossary
        self._ignore_list = '' if ignore_list is None else ignore_list
        self._writer = writer

    def _load(self, sdlxliffs):
        if Path(sdlxliffs).is_file():
            return [sdlxliffs]
        elif Path(sdlxliffs).is_dir():
            files = glob.glob(sdlxliffs + '/*.sdlxliff')

            if files is None or len(files) == 0:
                raise Exception("Could not find any file in the path provided.")
            else:
                return files
        else:
            raise Exception("The provided path does not exist.")

    def check_glossary(self):
        """ Main method for glossary consistency check.

        Checks if the target term is in the target segment if the source term
        is in the source segment.

        Yields
        ------
        CheckResult : namedtuple
            Contains sdlxliff and list of Problem namedtuple.

        """
        if self._glossary is None:
            raise Exception("At least one glossary excel file is required for glossary check.")

        results = list()

        for sdlxliff in self._sdlxliffs:
            gc = GlossaryChecker(sdlxliff, self._glossary, self._ignore_list)
            result = CheckResult(sdlxliff, gc.glossary_check())

            if self._writer == "excel":
                results.append(result)
            else:
                yield result

        if self._writer == "excel":
            write(results, self._writer)

    def check_length(self, **kwargs):
        """ Checks and finds segments with length discrepancy greater than set values.

        Parameters
        ----------
        min : float

            Minimum allowed threshold. If min is triggered, target is too short compared to source.

        max : float

            Maximum allowed threshold. If max is triggered, target is too long compared to source.

        source_min : int

            Minimum source length to show. This is to filter out item or character names that may be irrelevant.


        Yields
        ------
        DiscProblem
            A namedtuple containing discrepancy length, segment.mid, segment.source, segment.target.
        
        """
        for sdlxliff in self._sdlxliffs:
            yield check_length(sdlxliff, **kwargs)

    def rfilter(self, source=None, target=None):
        """ Filtering function with regex.
        
        Takes a regex expression for source and/or target.
        
        Paramters
        ---------
        source : str

            String to be included in the source.

        target : str

            String to be included in the target.
            

        Returns
        ------
        list of FilteredSegments
        """
        
        results = list()

        for sdlxliff in self._sdlxliffs:
            result = rfilter(sdlxliff, source, target)
            
            if result is not None:
                if self._writer == "excel":
                    results.append(result)
                else:
                    yield result

            if self._writer == "excel":
                write(results, self._writer)
            

if __name__ == "__main__":
    pass