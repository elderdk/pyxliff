from .helpers import (
    get_files,
    remove_partials,
    make_txt,
    analyze_segment
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
        print("from find_terms", self._files)
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
        r = dict()

        for xliff in xliffs:
            for segment in xliff.segments:
                d = analyze_segment(segment.source, max_lookup_length)
                for k, v in d.items():
                    if len(k) > 1:
                        if k not in r.keys():
                            r[k] = v
                        else:
                            r[k]['val'] += d[k]['val']
            self.progressed.emit(xliffs.index(xliff) + 1)
            self.termsFile.emit(str(xliff))

        r = {
            k: v for k, v in sorted(r.items(), key=lambda x: -x[1]['val'])
            if v['val'] >= min_match
            }

        r = remove_partials(r)
        if make_file and file_name is not None:
            make_txt(r, file_name)
        else:
            pp(r)

        self.progressed.emit(0)
        self.finished.emit()
