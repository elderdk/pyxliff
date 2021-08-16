# -*- coding: utf-8 -*-
# rprename/views.py

"""Provides the RP Renamer main window."""
from pathlib import Path

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from .terms_finder import TermsFinder
from .ui.window import Ui_Window


FILTERS = ";;".join(
    (
        "*.sdlxliff",
    )
)


class Window(QMainWindow, Ui_Window):
    def __init__(self):
        super().__init__()
        self._files = list()
        self._filesCount = len(self._files)
        self._setupUI()
        self._connectSignalsSlots()

    def _setupUI(self):
        self.setupUi(self)

    def _connectSignalsSlots(self):
        self.loadFilesButton.clicked.connect(self.loadFiles)
        self.findTermsButton.clicked.connect(self.findTerms)

    def loadFiles(self):
        self.filesListWindow.clear()
        initDir = str(Path.home())

        files, filter = QFileDialog.getOpenFileNames(
            self, "Choose Sdlxliff Files", initDir, filter=FILTERS
        )

        if len(files) > 0:
            for file in files:
                self._files.append(file)
                self.filesListWindow.addItem(file)
            self._filesCount = len(self._files)

    def findTerms(self):
        self._runFindTermsThread()

    def _runFindTermsThread(self):
        self._thread = QThread()
        min_match = self.minMatchValue.value()
        max_lookup_length = self.maxLookupLengthValue.value()

        self._finder = TermsFinder(
            self._files,
            "./terms_found.txt",
            min_match,
            max_lookup_length,
            True
        )

        self._finder.moveToThread(self._thread)
        self._thread.started.connect(self._finder.find_terms)
        # Clean up
        self._finder.finished.connect(self._thread.quit)
        self._thread.start()
