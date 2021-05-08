from pyxliff.tests.fixtures import sdlxliff


def test_sdlxliff_loading(sdlxliff):
    assert len(sdlxliff.segments) == 48


def test_sdlxliff_find_mid(sdlxliff):
    assert sdlxliff.find_mid(15).mid == 15


def test_sdlxliff_source(sdlxliff):
    assert sdlxliff.find_mid(17).source == "제3조 대한민국의 영토는 한반도와 그 부속도서로 한다."


def test_sdlxliff_target(sdlxliff):
    assert sdlxliff.find_mid(17).target == "Article 3 The territory of the Republic of Korea shall consist of the Korean peninsula and its adjacent islands."

def test_all_segments_contain_mid(sdlxliff):
    assert all([segment.mid for segment in sdlxliff.segments])