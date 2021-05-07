
class TermSegmentGroup:

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

    if not all([
        isinstance(source_term, str),
        isinstance(target_term, str),
    ]):
        return False

    source_term = source_term.split('|')
    target_term = target_term.split('|')
    source_segment = segment.source.lower()
    target_segment = segment.target.lower()

    tsg = TermSegmentGroup(
        source_term, target_term, source_segment, target_segment
        )

    if tsg.not_found_in_source:
        return False
    elif tsg.found_in_source_but_not_in_target:
        return True
    

# Codes here should do the actual checking.
def check(sdlxliff, glossary):
    # sdlxliff will come as a SdlXliff object with .source and .target.
    # glossary will come as a pandas dataframe
    
    i = 0
    for segment in sdlxliff.segments:
        for row_num, row in glossary.iterrows():

            source_term, target_term = row[0], row[1]
            
            problem = _lookin(source_term,target_term, segment)

            if problem:
                print(
                    f"{segment.mid}: {source_term}, {target_term}"
                    )
                i += 1
    print(f'total of {i} problems found.')

if __name__ == '__main__':
    pass