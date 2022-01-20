from .helpers import (
    get_files,
    remove_partials,
    make_txt,
    analyze_segment,
    _make_tmp,
    compare_and_compile_dict
)
from PyQt5.QtCore import QObject, pyqtSignal
from pathlib import Path
from pprint import pprint as pp


class TermsFinder(QObject):
    progressed = pyqtSignal(int)
    termsFile = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self,
                 files,
                 file_name,
                 min_match,
                 max_lookup_length,
                 make_file=True,
                 ):

        super().__init__()
        self._files = files,
        self._file_name = file_name,
        self._min_match = min_match,
        self._max_lookup_length = max_lookup_length,
        self._make_file = make_file,

    def find_terms(self):
        self.combined_analysis(
            get_files(self._files[0]),
            self._file_name[0],
            self._min_match[0],
            self._max_lookup_length[0],
            self._make_file[0]
        )

    def combined_analysis(self, xliffs: list, file_name, min_match: int, max_lookup_length: int, make_file: bool):
        """ Loops through all xliffs to create analyzed defaultdicts

        Loops through all xliffs to create analyzed defaultdicts and
        return a sorted, combined defaultdict.
        """
        tmpfile = _make_tmp()

        for xliff in xliffs:
            print("working on ", xliff)
            with tmpfile.open(mode='a', encoding='utf-8') as f:
                for segment in xliff.segments:
                    analyze_segment(segment.source, max_lookup_length, f)

                self.progressed.emit(xliffs.index(xliff) + 1)
                self.termsFile.emit(str(xliff))

        r = compare_and_compile_dict(min_match)
        print("length of r before remove_partials: ", len(r))
        r = remove_partials(r)  # blocking for now because this is taking too long. Need to reduce the number of keys in r.
        if make_file and file_name is not None:
            make_txt(r, file_name)
        else:
            pp(r)

        self.progressed.emit(0)
        self.finished.emit()
