from collections import namedtuple
from core.sdlxliff import SdlXliff
import re

FilteredSegment = namedtuple("FilteredSegment", "mid source target".split())


def rfilter(sdlxliff, source, target):

    # returns bool
    def _found(segment, source, target):

        if source is None and target is not None:
            return re.match(target, segment.target)
        elif source is not None and target is None:
            return re.match(source, segment.source)
        elif source is None and target is None:
            return None
        else:
            return (
                re.match(source, segment.source) and 
                re.match(target, segment.target)
            )

    sdlxliff = SdlXliff(sdlxliff)

    result = [
        FilteredSegment(segment.mid, segment.source, segment.target)
        for segment in sdlxliff.segments
        if _found(segment, source, target)
    ]

    return result


if __name__ == "__main___":
    pass