from core.sdlxliff import SdlXliff
from pathlib import Path
from pprint import pprint as pp
import random
import string
from collections import Counter
from time import sleep


TEMP_FOLDER = './tmp'
MASTER_FILE = './terms_found.txt'


def get_context(text, key):
    return text[text.index(key) - 20: text.index(key) + len(key) + 20]


def get_files(files):
    return [SdlXliff(file) for file in files]


def _make_tmp():

    def _get_fname():
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(20))

    tmp_folder = Path(TEMP_FOLDER)

    if not tmp_folder.exists():
        tmp_folder.mkdir()

    full_path = tmp_folder.joinpath(_get_fname())
    Path(full_path).touch()

    return Path(full_path)


def save_to_tmp(key, context, f):
    # currently not using context. Should be removed later.
    f.write(key + '\n')
    

def analyze_segment(text, max_lookup_length, f):
    """ Creates a defaultdict(int) that shows the count of repeated
        words and phrases

    """

    for n in range(2, max_lookup_length):
        for i in range(0, len(text)):
            if not i+n+1 > len(text):
                key = text[i:i+n+1]
                if not key.startswith(' ') and not key.endswith(' '):  # prevents same things from being added just becaus they are same when stripped
                    if len(key) < 5 and ' ' in key:  # if shorter than 6 but includes a space, it is considered a meaningless partial and skipped
                        continue
                    save_to_tmp(key, get_context(text, key), f)


def compare_and_compile_dict(min_match):
    """Goes through tmp files in tmp folder and create a dict.
    
    The dict will contain all keys that match more than the min_match value.
    """
    tmp_files = Path(TEMP_FOLDER).glob('*')
    cnt = Counter()

    for tmp_file in tmp_files:
        keys = list()
        
        # creates a list of all keys in the tmp_file
        with tmp_file.open() as f:
            last_line = ""
            lines = f.readlines()
            for line in lines[::-1]:
                if line in last_line:
                    continue
                keys.append(line.strip())
                last_line = line
        cnt.update(keys)
        tmp_file.unlink()

    
    return {k: v for k, v in cnt.items() if v >= min_match}
            

def remove_partials(dd):

    keys1 = [key for key in dd.keys()]
    keys2 = [key for key in dd.keys()]
    for key1 in keys1:
        for key2 in keys2:
            if key1 in key2 and key1 != key2 and key1 in dd:
                dd.pop(key1)

    return dd


def make_txt(dd, file_name):
    with open(file_name, mode='w', encoding="utf-8") as f:
        for k, v in dd.items():
            f.write(f"{v}: {k}\n")
