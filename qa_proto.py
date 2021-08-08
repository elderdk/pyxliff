from core.sdlxliff import SdlXliff
from collections import defaultdict
from pathlib import Path
from pprint import pprint as pp

test_xliff = r"C:\Users\danielelder\Documents\Studio 2019\Projects\제1차_자율주행_교통물류_기본계획_1\en-US\제1차_자율주행_교통물류_기본계획_prep.docx.sdlxliff"
test_path = r"C:\Users\danielelder\Documents\Studio 2019\Projects\priority 2\en-US"
FILE_NAME = './terms_found.txt'
rok_const = r"pyxliff\tests\testdata\rok_const.sdlxliff"
neo = r"C:\Users\danielelder\Documents\Studio 2019\Projects\200709_Log Analysis_Ragnarok Crusade - KO2EN\en-US"


def get_files(path):

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError

    if path.is_file():
        return [SdlXliff(path)]
    elif path.is_dir():
        return [SdlXliff(xliff) for xliff in path.glob('*.sdlxliff')]

def analyze_segment(text, max_loopkup_length):
    """ Creates a defaultdict(int) that shows the count of repeated
        words and phrases

    """
    d = defaultdict(int)
    last_entry = ''

    for n in range(2, max_loopkup_length):
        for i in range(0, len(text)):
            if not i+n+1 > len(text):
                key = text[i:i+n+1]
                if not key.startswith(' ') and not key.endswith(' '): #prevents same things from being added just becaus they are same when stripped
                    if len(key) < 5 and ' ' in key: #if shorter than 6 but includes a space, it is considered a meaningless partial and skipped
                        continue
                    d[key] += 1
                    if last_entry != '' and last_entry in key and last_entry in d.keys(): # checks the last entry and if the current entry includes the last entry, it is deleted.
                        d.pop(last_entry)
                    last_entry = key
    return d


def remove_partials(dd):

    keys1 = [key for key in dd.keys()]
    keys2 = [key for key in dd.keys()]
    print(f"{len(keys1) * len(keys2)}")
    for key1 in keys1:
        for key2 in keys2:
            if key1 in key2 and key1 != key2 and key1 in dd:
                dd.pop(key1)

    return dd


def make_txt(dd):
    with open(FILE_NAME, mode='w', encoding="utf-8") as f:
        for k, v in dd.items():
            f.write(f"{v}\t{k}\n")


def combined_analysis(xliffs: list, min_match: int = 2, max_loopkup_length: int = 50, make_file: bool = True):
    """ Loops through all xliffs to create analyzed defaultdicts

    Loops through all xliffs to create analyzed defaultdicts and
    return a sorted, combined defaultdict.
    """
    r = defaultdict(int)

    for xliff in xliffs:
        print(f"Working on {xliff}")
        for segment in xliff.segments:
            d = analyze_segment(segment.source, max_loopkup_length)
            for k, v in d.items():
                if len(k) > 1:
                    r[k] += v

    r = {
        k: v for k, v in sorted(r.items(), key=lambda x: -x[1])
        if v >= min_match
        }

    r = remove_partials(r)
    if make_file:
        make_txt(r)
    else:
        pp(r)


if __name__ == '__main__':
    # add context (20 chars before and after the find) to the dict
    combined_analysis(
        get_files(test_path),
        min_match=10,
        max_loopkup_length = 50,
        make_file=True)
