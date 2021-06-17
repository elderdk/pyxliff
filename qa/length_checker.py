from numpy import mean
from core.sdlxliff import SdlXliff
from collections import namedtuple
from math import floor


DiscProblem = namedtuple('DiscProblem', 'disc mid source target'.split(' '))


def check_length(sdlxliff, min=0.2, max=1.3, source_min=10):

    def _get_disc(segment):
        return round(len(segment.target) / len(segment.source), 2)
    
    def _get_average_discrepancy(sdlxliff):

        discrepancies = [
            _get_disc(segment) for segment in sdlxliff.segments
        ]

        return mean(discrepancies)

    sdlxliff = SdlXliff(sdlxliff)
    average_disc = _get_average_discrepancy(sdlxliff)

    min = average_disc * min
    max = average_disc * max

    result = [
        DiscProblem(_get_disc(segment), segment.mid, segment.source, segment.target)
        for segment in sdlxliff.segments
        if min < _get_disc(segment) > max and len(segment.source) >= source_min
        ]

    return result