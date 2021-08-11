from core.sdlxliff import SdlXliff
from pathlib import Path
from pprint import pprint as pp


def get_context(text, key):
    return text[text.index(key) - 20: text.index(key) + len(key) + 20]


def get_files(files):
    print("from get_files", files)
    return [SdlXliff(file) for file in files]


def analyze_segment(text, max_lookup_length):
    """ Creates a defaultdict(int) that shows the count of repeated
        words and phrases

    """
    d = dict()
    last_entry = ''

    for n in range(2, max_lookup_length):
        for i in range(0, len(text)):
            if not i+n+1 > len(text):
                key = text[i:i+n+1]
                if not key.startswith(' ') and not key.endswith(' '):  # prevents same things from being added just becaus they are same when stripped
                    if len(key) < 5 and ' ' in key:  # if shorter than 6 but includes a space, it is considered a meaningless partial and skipped
                        continue
                    if key not in d.keys():
                        d[key] = dict()
                        d[key]['val'] = 1
                        d[key]['context'] = get_context(text, key)
                    else:
                        d[key]['val'] += 1
                        d[key]['context'] = get_context(text, key)
                    if last_entry != '' and last_entry in key and last_entry in d.keys():  # checks the last entry and if the current entry includes the last entry, it is deleted.
                        d.pop(last_entry)
                    last_entry = key
    return d


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
            f.write(f"{v['val']}*{k}*{v['context']}\n")
