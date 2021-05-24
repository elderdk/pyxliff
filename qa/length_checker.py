from numpy import mean
from core.sdlxliff import SdlXliff
from collections import namedtuple
from math import floor


DiscProblem = namedtuple('DiscProblem', 'disc mid source target'.split(' '))


def check_length(sdlxliff, min=0.2, max=1.3, source_min=10):
    """ Checks if target length is too long or short compared to source.

    Checks if the target segment length is too long or too short compared to its 
    source counterpart. 'Too long' or 'too short' is determined by parameters
    that define the minimum and maximum percentage points compared to the 'average'
    length discrepancy of the entire file.

    Parameters
    ----------
    sdlxliff : Sdlxliff
        The Sdlxliff object to check.
    min : float
        Minimum percentage discrepenacy allowed.
    max : int
        Maximum percentage discrepancy allowed.
    source_min : int
        Minimum length of the source sergment. This is to filter out characters and
        item names.
    """

    def _load_sdlxliff(sdlxliff):
        return SdlXliff(sdlxliff)

    def _get_disc(segment):
        return round(len(segment.target) / len(segment.source), 2)
    
    def _get_average_discrepancy(sdlxliff):

        discrepancies = [
            _get_disc(segment) for segment in sdlxliff.segments
        ]

        return mean(discrepancies)

    sdlxliff = _load_sdlxliff(sdlxliff)
    average_disc = _get_average_discrepancy(sdlxliff)

    min = average_disc * min
    max = average_disc * max

    result = [
        DiscProblem(_get_disc(segment), segment.mid, segment.source, segment.target)
        for segment in sdlxliff.segments
        if min < _get_disc(segment) > max and len(segment.source) >= source_min
        ]

    return result