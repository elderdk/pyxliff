from pyxliff.tests.fixtures import glossary_checker as gc


def test_glossarychecker_load():
    assert gc


def test_glossary_len(gc):
    assert len(gc.glossary_check()) == 16


def test_glossary_problem(gc):
    problem = gc.glossary_check()[0]
    assert problem.mid == 5 and problem.source_term == ['헌법']
