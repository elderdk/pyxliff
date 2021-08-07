from core.sdlxliff import SdlXliff
from collections import Counter, defaultdict

test_xliff = r"C:\Users\elder\Documents\python\pyxliff\pyxliff\tests\testdata\rok_const.sdlxliff"
TEST_STRING = "피고인의 자백이 고문ㆍ폭행ㆍ협박"

xliff = SdlXliff(test_xliff)

def create_d(text):
    d = defaultdict(int)
    for n in range(2, len(text)):
        for i in range(0, len(text)):
            if not i+n+2 > len(text):
                key = text[i:i+n].strip()
                d[key] += 1
    return d

r = defaultdict(int)

for segment in xliff.segments:
    d = create_d(segment.source)
    for k, v in d.items():
        if len(k) > 1:
            r[k] += v

print(Counter(r).most_common(30))