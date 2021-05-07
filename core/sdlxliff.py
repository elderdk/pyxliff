from bs4 import BeautifulSoup
import glob
from .segment import Segment


class SdlXliff:
    """Core object from which tasks can be performed.

    This is the core object created from a sdlxliff file. It takes a string,
    which derives from a sdlxliff file, and uses BeautifulSoup to parse the
    xml in the file for further processing.

    """

    def __init__(self, sdlxliff: str):
        """

        Parameters
        ----------
        sdlxliff : str
            The string representation of the sdlxliff file.
            Make sure to pass it in a string format.
            
            Example

                    file = open(path_to_file).read()
                    to_bytes = bytes(file, 'UTF-8')
                    sdlxliff = SdlXliff(to_bytes)
        

        """
        self.__soup = BeautifulSoup(sdlxliff, 'lxml')

    def __get_segments(self) -> list:
        return [
           Segment(unit) for unit in self.__soup.find_all("trans-unit")
           if unit.mrk
        ]

    @property
    def segments(self) -> list:
        """list: A list of segments which are Segment objects. """
        return self.__get_segments()

    def find_mid(self, mid: int) -> Segment:
        """Returns a Segment object (segment) with the same mid number. 
        
        Parameters
        ----------
        mid : int
            mid is the 'segment number' seen in Studio.
            Use this function to find the segment with the 'segment number' 
            you are looking for.

        Returns
        -------
        Segment
        
        """
        for segment in self.segments:
            if segment.mid == int(mid):
                return segment


if __name__ == '__main__':

    file = open(glob.glob('./pyxliff/tests/testdata/*.sdlxliff')[0]).read()
    to_bytes = bytes(file, 'UTF-8')
    sdlxliff = SdlXliff(to_bytes)

    
