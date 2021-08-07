from core.sdlxliff import SdlXliff
from collections import Counter, defaultdict

test_xliff = r"C:\Users\elder\Documents\python\pyxliff\pyxliff\tests\testdata\rok_const.sdlxliff"
TEST_STRING = "피고인의 자백이 고문ㆍ폭행ㆍ협박"

xliff = SdlXliff(test_xliff)


def analyze_segment(text):
    """ Creates a defaultdict(int) that shows the count of repeated words and phrases

    """
    d = defaultdict(int)
    for n in range(2, len(text)):
        for i in range(0, len(text)):
            if not i+n+1 > len(text):
                key = text[i:i+n+1]
                if not key.startswith(' ') and not key.endswith(' '):
                    d[key] += 1
    return d

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

    r = {k: v for k, v in sorted(r.items(), key=lambda x: -x[1])}

    return remove_partials(r)

def remove_partials(dd):
    # if dd key contains a space, check it through all other keys. If it's included in another key, remove the shorter one.
    keys = [key for key in dd.keys()] 

    for i in range(0, len(keys)):
        for n in range(1, len(keys)):
            
            if (
                not n > len(keys)+1 and
                keys[i] in keys[i+n] and 
                len(keys[i]) != len(keys[i+n]) and 
                keys[i] in dd
                ):
                print(keys[i])
                dd.pop(keys[i])

    return dd

r = combined_analysis([xliff])

for k, v in r.items():
    if v > 3:
        print(v, k)