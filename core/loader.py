from pathlib import Path
import glob
from collections import namedtuple

from glossary.glossarychecker import GlossaryChecker
from qa.length_checker import check_length


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

    Methods
    -------
    glossary_check()
        Main method for glossary consistency check.
        Checks if the target term is in the target segment if the source term
        is in the source segment.


    """

    def __init__(self, sdlxliffs, glossary=None, ignore_list=None):
        self._sdlxliffs = self._load(sdlxliffs)
        self._glossary = glossary
        self._ignore_list = '' if ignore_list is None else ignore_list

    
    def _load(self, sdlxliffs):
        if Path(sdlxliffs).is_file():
            return [sdlxliffs]
        elif Path(sdlxliffs).is_dir():
            files = glob.glob(sdlxliffs + '/*.sdlxliff')

            if files is None or len(files) == 0:
                raise Exception("Could not find any file in the path provided.")
            else:
                return files

    def check_glossary(self):
        """
        
        Yields
        ------
        CheckResult : namedtuple
            Contains sdlxliff and list of Problem namedtuple.

        """
        if self._glossary is None:
            raise Exception("At least one glossary excel file is required for glossary check.")

        for sdlxliff in self._sdlxliffs:
            gc = GlossaryChecker(sdlxliff, self._glossary, self._ignore_list)
            result = CheckResult(sdlxliff, gc.glossary_check())
            yield result

    def check_length(self, **kwargs):
        """

        Yields
        ------
        
        """
        for sdlxliff in self._sdlxliffs:
            yield check_length(sdlxliff, **kwargs)

            

if __name__ == "__main__":
    c = r"C:\Users\danielelder\Desktop\dump\lost_memories_update\0_Source\Studio"
    ll = Loader(c)
    print(ll._sdlxliffs)