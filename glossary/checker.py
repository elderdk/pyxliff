from collections import namedtuple
import multiprocessing
from itertools import product


Problem = namedtuple('Problem', 'mid,source_term,target_term'.split(','))


class TermSegmentGroup:
    """Object that sets up the individual terms and segments for comparison.

    This object takes the source and target terms from one row of the glossary,
    and prepare it to be compared with an individual source and target segment pair.
    It has properties designed to easily distinguish the comparison result.

    Parameters
    ----------
    source_terms : list
        List of terms. Since _lookin splits the term with '|', the terms will come
        as a list even if there is only one term.

    target_terms : list
        Same as source_terms.

    source_segment : str
        String of source segment.
    
    target_segment : str
        Same as source_segment.


    Attributes
    ----------
    found_in_source_but_not_in_target : bool
        A source term is found in the source segment but the corresponding target term
        is not found in the target segment, indicating the possibility that
        an incorrect term has been used.

    not_found_in_source : bool
        Self explanatory. To be used to tell _lookin to skip the term.
    
    """

    def __init__(self, source_terms, target_terms, source_segment, target_segment):
        self._source_terms = source_terms
        self._target_terms = target_terms
        self._source_segment = source_segment
        self._target_segment = target_segment

    @property
    def _term_found_in_source(self):
        return any(
            [
                term in self._source_segment 
                for term in self._source_terms
                ]
            )

    @property
    def _term_found_in_target(self):
        return any(
            [
                term in self._target_segment 
                for term in self._target_terms
                ]
            )

    @property
    def found_in_source_but_not_in_target(self):
        return (
            self._term_found_in_source and
            not self._term_found_in_target
        )

    @property
    def not_found_in_source(self):
        return (
            not self._term_found_in_source
        )


def seg_looper(segment, row):

    row_contents = row[1]

    # Some cells return NaN value, making it a float, not str, and skipped by the below if condition.
    if not isinstance(row_contents[0], str) or not isinstance(row_contents[1], str):
        return None

    data = {
    'source_terms': [term.lower() for term in row_contents[0].split('|')],
    'target_terms': [term.lower() for term in row_contents[1].split('|')],
    'source_segment': segment.source.lower(),
    'target_segment': segment.target.lower()
    }

    tsg = TermSegmentGroup(**data)

    if tsg.found_in_source_but_not_in_target:
        return Problem(segment.mid, data['source_terms'], data['target_terms'])


def check(sdlxliff, glossary, ignore_list):
    """Main function that does the glossary checking.
    
    This function uses multiprocessing to speed up the process. It first uses itertools'
    product() function to create a generator that yields tuples with a sdlxliff.segment object
    and a Pandas DataSeries (called row). Then the multiprocessor.Pool().starmap is used
    to pass each tuple to the seg_looper() which uses lookin() to determine if
    the source term is in the source segment but target term is not in the target segment.
    If a problem is found, the starmap() will return a Problem namedtuple object which are
    apended to the results list.

    Parameters
    ----------
    sdlxliff : SdlXliff object
        SdlXliff object that contains source and target segments.

    glossary : Pandas DataFrame
        Pandas DataFrame object that contains source and target terms.
        Duplicate terms are concanated in one cell, joined by '|' which is then
        splitted in _lookin function.

    """
    
    import time
    start_time= time.time()
    products = product(
        sdlxliff.segments, 
        [row for row in glossary.iterrows() if row[1][0] not in ignore_list],
        repeat=1
        )
    print(f"{time.time() - start_time} seconds")

    # test the below with above with a big glossary file and a sdlxliff and see which performs better.

    # import time
    # start_time= time.time()
    # rows = [row for row in glossary.iterrows() if row[1][0] not in ignore_list]
    # products = ((segment, row) for segment in sdlxliff.segments for row in rows)
    # print(f"{time.time() - start_time} seconds")

    with multiprocessing.Pool() as pool:
        results = [
            result for result in pool.starmap(seg_looper, products)
            if result is not None
            ]


    print(f'total of {len(results)} problems found.')
    return sorted(results, key=lambda x: x.mid)

if __name__ == '__main__':
    pass