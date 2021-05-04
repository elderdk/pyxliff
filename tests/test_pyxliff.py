import glob
import pytest

from pyxliff.models import SdlXliff


@pytest.fixture
def sdlxliff():
    file = open(glob.glob('./pyxliff/tests/testdata/*.sdlxliff')[0]).read()
    to_bytes = bytes(file, 'UTF-8')
    sdlxliff = SdlXliff(to_bytes)
    return sdlxliff


def test_sdlxliff_loading(sdlxliff):
    assert len(sdlxliff.segments) == 49


def test_sdlxliff_find_mid(sdlxliff):
    assert sdlxliff.find_mid(15)


def test_sdlxliff_source(sdlxliff):
    assert sdlxliff.find_mid(17).source == "제3조 대한민국의 영토는 한반도와 그 부속도서로 한다."


def test_sdlxliff_target(sdlxliff):
    assert sdlxliff.find_mid(17).target == "Article 3 The territory of the Republic of Korea shall consist of the Korean peninsula and its adjacent islands."
