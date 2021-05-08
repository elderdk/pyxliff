from pyxliff.tests.fixtures import glossary, sdlxliff


def test_glossarychecker_load(glossary):
    assert glossary

def test_glossary_len(glossary):
    assert len(glossary.check()) == 16

def test_glossary_problem(glossary):
    problem = glossary.check()[0]
    assert problem.mid == 5 and problem.source_term == '헌법'
