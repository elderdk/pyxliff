

class Segment:
    """Basic segment object containing its source and target texts.

    This is the most basic segment block which is used for the parsed
    'trans-unit' tags in the sdlxliff file.

    Parameters
    ----------
    tag : Tag
        A BeautifulSoup tag.

    Attributes
    ----------
    mid : int
        mid is the 'segment number' as seein in Studio.

    source : str
        The source text. If empty, '' will be returned.

    target : str
        The target text. If empty, '' will be returend.
        
    """

    def __init__(self, tag):

        self.mid = self.__get_mid(tag)
        self.source = tag.source.get_text()
        self.target = tag.target.get_text()

    def __get_mid(self, tag) -> int:
        try:
            mid = tag.target.mrk['mid']
            mid = int(mid)

        except(TypeError):
            mid = 'None'

        return mid

    def __repr__(self):
        return f"""
        mid   : {self.mid}
        source: {self.source}
        target: {self.target}
        """