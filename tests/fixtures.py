import pytest
import glob

from pyxliff.core.sdlxliff import SdlXliff
from pyxliff.glossary.glossarychecker import GlossaryChecker


TEST_SDLXLIFF = r"C:\Users\elder\Documents\python\pyxliff\pyxliff\tests\testdata\rok_const.sdlxliff"
TEST_GLOSSARY = r"C:\Users\elder\Documents\python\pyxliff\pyxliff\tests\testdata\excel_glossary.xlsx"
IGNORE_LIST = '게'

@pytest.fixture
def sdlxliff():
    file = open(glob.glob(TEST_SDLXLIFF)[0], encoding='UTF-8').read()
    sdlxliff = SdlXliff(bytes(file, 'UTF-8'))
    return sdlxliff


@pytest.fixture
def glossary(sdlxliff):
    return GlossaryChecker(TEST_SDLXLIFF, TEST_GLOSSARY, IGNORE_LIST)
