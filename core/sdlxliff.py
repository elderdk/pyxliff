from bs4 import BeautifulSoup
import glob
from .segment import Segment
from pathlib import Path


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
            It should be only one file.
            
            Example

                    file = open(path_to_file).read()
                    to_bytes = bytes(file, 'UTF-8')
                    sdlxliff = SdlXliff(to_bytes)
        

        """
        self._sdlxliff_name = Path(sdlxliff).name
        self.__sdlxliff = self.__load_sdlxliff(sdlxliff)
        self.__soup = BeautifulSoup(self.__sdlxliff, 'lxml')

    def __get_segments(self) -> list:
        return [
           Segment(unit) for unit in self.__soup.find_all("trans-unit")
           if unit.mrk
        ]

    def __load_sdlxliff(self, sdlxliff):
        fi = open(sdlxliff, encoding='UTF-8').read()
        return bytes(fi, 'UTF-8')

    @property
    def segments(self) -> list:
        """list: A list of segments which are Segment objects. """
        return self.__get_segments()

    @property
    def name(self) -> str:
        """str: The name of the sdlxliff file."""
        return self._sdlxliff_name

    def find_mid(self, mid: int) -> list:
        """Returns a list of Segment objects (segment) with the same mid number. 
        
        Parameters
        ----------
        mid : int
            mid is the 'segment number' seen in Studio.
            Use this function to find the segment with the 'segment number' 
            you are looking for.

        Returns
        -------
        A matching Segment object
        
        """
        return [segment for segment in self.segments if segment.mid == int(mid)]

    def filter(self):
        """
        Returns a list of segments that 
        """
        pass

if __name__ == '__main__':
    pass
    
