from collections import namedtuple
import multiprocessing
import tqdm


Problem = namedtuple('Problem', 'mid,source_term,target_term'.split(','))


def seg_looper(segment, row):

    def _found_in_source_but_not_in_target(data):
        return any(
            [
                term in data['source_segment'] for term in data['source_terms']
                ]
            ) and not any(
            [
                term in data['target_segment'] for term in data['target_terms']
                ]
            )

    row_contents = row[1]

    data = {
        'source_terms': [term.lower() for term in row_contents[0].split('|')],
        'target_terms': [term.lower() for term in row_contents[1].split('|')],
        'source_segment': segment.source.lower(),
        'target_segment': segment.target.lower()
    }

    if _found_in_source_but_not_in_target(data):

        return Problem(segment.mid, data['source_terms'], data['target_terms'])


def check(sdlxliff, glossary, ignore_list):
    """Main function that does the glossary checking.

    This function uses multiprocessing to speed up the process. It first
    creates a generator that yields tuples with a sdlxliff.segment object and
    a Pandas DataSeries (called row). Then the multiprocessor.Pool().starmap
    is used to pass each tuple to the seg_looper() which uses lookin() to
    determine if the source term is in the source segment but target term is
    not in the target segment. If a problem is found, the starmap() will
    return a Problem namedtuple object which are apended to the results list.

    Parameters
    ----------
    sdlxliff : SdlXliff object
        SdlXliff object that contains source and target segments.

    glossary : Pandas DataFrame
        Pandas DataFrame object that contains source and target terms.
        Duplicate terms are concanated in one cell, joined by '|' which is then
        splitted in _lookin function.

    """

    # get the rows that are not NaN and not included in the ignore_list
    terms = [
        row for row in glossary.iterrows()
        if all([isinstance(row[1][0], str), isinstance(row[1][1], str)]) and
        not any([term in ignore_list for term in row[1][0].split('|')])
        ]

    # list for the segment-row pair
    products = [
        (segment, term) for segment in sdlxliff.segments for term in terms
        ]

    with multiprocessing.Pool() as pool:

        results = [
            result for result in pool.starmap(
                seg_looper,
                tqdm.tqdm(
                    products, desc=sdlxliff.name,
                    bar_format='{l_bar}{bar:20}{r_bar}{bar:-10b}',
                    total=len(products)
                    )
                ) if result is not None
            ]

    return sorted(results, key=lambda x: x.mid)


if __name__ == '__main__':
    pass
