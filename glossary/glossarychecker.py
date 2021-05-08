from .maker import make
from .checker import check
from core.sdlxliff import SdlXliff


class GlossaryChecker:
    """Core object for glossary checking.

    This is the core object for glossary checking.

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

            Example

                ignore_list = "apple,pear,banana"

        """
        self._info = [sdlxliff, glossary]
        self._sdlxliff = self._import_sdlxliff(sdlxliff)
        self._glossary = self._import_glossary(glossary)
        self._ignore_list = ignore_list.split(',')

    def _import_sdlxliff(self, sdlxliff):
        file = open(sdlxliff, encoding='UTF-8').read()
        return SdlXliff(bytes(file, 'UTF-8'))

    def _import_glossary(self, glossary):
        return make(glossary)

    @property
    def segments(self):
        """list: A list of segments which are Segment objects."""
        return self._sdlxliff.segments

    def check(self):
        """Calls the check function in checker.py
        """
        return check(self._sdlxliff, self._glossary, self._ignore_list)

    def __repr__(self):
        return f"""
        sdlxliff: {self._info[0]}
        glossary: {self._info[1]}
        """


if __name__ == '__main__':
    pass