from collections import namedtuple


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
        self._source_segment = source_segment.lower()
        self._target_segment = target_segment.lower()

    @property
    def _term_found_in_source(self):
        return any(
            [
                term.lower() in self._source_segment 
                for term in self._source_terms
                ]
            )

    @property
    def _term_found_in_target(self):
        return any(
            [
                term.lower() in self._target_segment 
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


def _lookin(source_term, target_term, segment):
    """Function that looks into each segment and determines if term is used correctly.

    This function looks into each segment and determines if the source term is used in the source
    segment and if so, checks if the target term is used in the segment target.

    Parameters
    ----------
    source_term : str
    target_term : str
    segment : Segment object

    Returns
    -------
    bool

    """

    if not all([
        isinstance(source_term, str),
        isinstance(target_term, str),
    ]):
        return False

    source_terms = source_term.split('|')
    target_terms = target_term.split('|')
    source_segment = segment.source.lower()
    target_segment = segment.target.lower()

    tsg = TermSegmentGroup(
        source_terms, target_terms, source_segment, target_segment
        )

    if tsg.not_found_in_source:
        return False
    elif tsg.found_in_source_but_not_in_target:
        return True
    

def check(sdlxliff, glossary, ignore_list):
    """Main function that does the glossary checking.

    This is the main function used by the GlossaryChecker object. It processes each segment,
    and for each segment, it loops all the glossary terms in the glossary file.
    The _lookin function investigates to see if the segment.source contains the source term,
    and if so, checks if the corresponding target term has been used in the segment.target.
    If the target term is not found, _lookin returns True (varluable: problem) and
    prints out an error message.

    Parameters
    ----------
    sdlxliff : SdlXliff object
        SdlXliff object that contains source and target segments.

    glossary : Pandas DataFrame
        Pandas DataFrame object that contains source and target terms.
        Duplicate terms are concanated in one cell, joined by '|' which is then
        splitted in _lookin function.

    """
    Problem = namedtuple('Problem', 'mid,source_term,target_term'.split(','))
    i = 0
    result = []
    for segment in sdlxliff.segments:
        for row_num, row in glossary.iterrows():

            source_term, target_term = row[0], row[1]

            if source_term in ignore_list:
                continue
            
            problem = _lookin(source_term,target_term, segment)

            if problem:
                result.append(Problem(segment.mid, source_term, target_term))
                i += 1
    print(f'total of {i} problems found.')
    return result

if __name__ == '__main__':
    pass