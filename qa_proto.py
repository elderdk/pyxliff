from core.sdlxliff import SdlXliff
from collections import defaultdict

test_xliff = r"pyxliff/tests/testdata/rok_const.sdlxliff"
FILE_NAME = './terms_found.txt'
xliff = SdlXliff(test_xliff)


def analyze_segment(text):
    """ Creates a defaultdict(int) that shows the count of repeated
        words and phrases

    """
    d = defaultdict(int)
    for n in range(2, len(text)):
        for i in range(0, len(text)):
            if not i+n+1 > len(text):
                key = text[i:i+n+1]
                if not key.startswith(' ') and not key.endswith(' '):
                    d[key] += 1
    return d


def remove_partials(dd):

    keys1 = [key for key in dd.keys()]
    keys2 = [key for key in dd.keys()]

    for key1 in keys1:
        for key2 in keys2:
            if key1 in key2 and key1 != key2 and key1 in dd:
                dd.pop(key1)

    return dd


def make_txt(dd):
    with open(FILE_NAME, mode='a') as f:
        for k, v in dd.items():
            f.write(f"{v}, {k}\n")


def combined_analysis(xliffs: list):
    """ Loops through all xliffs to create analyzed defaultdicts

    Loops through all xliffs to create analyzed defaultdicts and
    return a sorted, combined defaultdict.
    """
    r = defaultdict(int)

    for xliff in xliffs:
        for segment in xliff.segments:
            d = analyze_segment(segment.source)
            for k, v in d.items():
                if len(k) > 1:
                    r[k] += v

    r = {
        k: v for k, v in sorted(r.items(), key=lambda x: -x[1])
        if v > 1
        }

    make_txt(remove_partials(r))


if __name__ == '__main__':
    combined_analysis([xliff])
