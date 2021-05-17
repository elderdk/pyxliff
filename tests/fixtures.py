import pytest
import glob

from pyxliff.core.sdlxliff import SdlXliff
from pyxliff.glossary.glossarychecker import GlossaryChecker


TEST_SDLXLIFF = r"tests\testdata\rok_const.sdlxliff"
TEST_GLOSSARY = r"tests\testdata\excel_glossary.xlsx"
IGNORE_LIST = '게'

@pytest.fixture
def sdlxliff():
    return SdlXliff(TEST_SDLXLIFF)


@pytest.fixture
def glossary_checker(sdlxliff):
    return GlossaryChecker(TEST_SDLXLIFF, TEST_GLOSSARY, IGNORE_LIST)
