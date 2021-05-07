from .maker import make
from .checker import check
from core.sdlxliff import SdlXliff


class GlossaryChecker:

    def __init__(self, sdlxliff, glossary, ignore_list):
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
        return self._sdlxliff.segments

    def check(self):
        check(self._sdlxliff, self._glossary, self._ignore_list)

    def __repr__(self):
        return f"""
        sdlxliff: {self._info[0]}
        glossary: {self._info[1]}
        """


if __name__ == '__main__':
    pass