from pyxliff.tests.fixtures import sdlxliff


def test_sdlxliff_loading(sdlxliff):
    assert len(sdlxliff.segments) == 48


def test_sdlxliff_find_mid(sdlxliff):
    assert sdlxliff.find_mid(15)[0].mid == 15

def test_sdlxliff_target(sdlxliff):
    assert sdlxliff.find_mid(17)[0].target == "Article 3 The territory of the Republic of Korea shall consist of the Korean peninsula and its adjacent islands."

def test_all_segments_contain_mid(sdlxliff):
    assert all([segment.mid for segment in sdlxliff.segments])