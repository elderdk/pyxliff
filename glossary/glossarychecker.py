from .maker import make
from .checker import check
from core.sdlxliff import SdlXliff
from collections import Counter, defaultdict
from pathlib import Path
import glob
from pandas import DataFrame


class GlossaryChecker:
    """Core object for glossary checking.

    This is the core object for glossary checking.

    Methods
    -------
    check()
        Returns CheckResult namedtuple containing the sdlxliff name
        and a list of Problem namedtuple.

    most_common(n:int):
        Returns the n number of most common Problem found, mainly
        to provide a visibility for recurring problems and false positives.

    """

    def __init__(self, sdlxliff, glossary, ignore_list):
        """

        Parameters
        ----------
        sdlxliff : str
            The string representation of the sdlxliff file path.
            It should be only one file.
        
        glossary : str
            The string representation of the glossary file path.
            For now, it supports only .xlsx files.
            It should be only one file.

        ignore_list : str
            A string of words that should be ignored separated by a comma.

        """
        self._info = [sdlxliff, glossary]
        self._sdlxliff = self._import_sdlxliff(sdlxliff)
        self._glossary = self._import_glossary(glossary)
        self._ignore_list = ignore_list.split(',')
        self._check_result = None

    def _import_sdlxliff(self, sdlxliff):
        return SdlXliff(sdlxliff)

    def _import_glossary(self, glossary):

        if Path(glossary).is_file():
            return make(glossary)
        elif Path(glossary).is_dir():

            glossaries = glob.glob(glossary + '/*.xlsx')

            if glossaries is None or len(glossaries) == 0:
                raise Exception("Could not find any glossary file in the path provided.")

            combined_glossary = DataFrame()

            for glossary in glossaries:
                if combined_glossary.empty:
                    combined_glossary = make(glossary)
                else:
                    combined_glossary = combined_glossary.append(make(glossary))

            return combined_glossary

    @property
    def segments(self):
        """list: A list of segments which are Segment objects."""
        return self._sdlxliff.segments

    def check(self):
        """Calls the check function in checker.py
        """
        self._check_result = check(self._sdlxliff, self._glossary, self._ignore_list)

        return self._check_result

    def most_common(self, n):

        if self._check_result is not None:
            cnt = Counter()
            for problem in self._check_result:
                cnt[problem.source_term[0]] += 1

        else:
            self.check()
            self.most_common(n)

        return cnt.most_common(n)

    def __repr__(self):
        return f"""
        sdlxliff: {self._info[0]}
        glossary: {self._info[1]}
        """


if __name__ == '__main__':
    pass