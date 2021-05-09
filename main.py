from glossary.glossarychecker import GlossaryChecker
import time

test_sdlxliff = r"C:\Users\elder\Documents\python\pyxliff\pyxliff\tests\testdata\rok_const.sdlxliff"
test_glossary = r"C:\Users\elder\Documents\python\pyxliff\pyxliff\tests\testdata\excel_glossary.xlsx"

current_sdlxliff = r"C:\Users\danielelder\Desktop\dump\lost_memories_update\0_Source\Studio\en-US\LanguageStd_2021.04.14.ver.xlsx.sdlxliff"
current_glossary = r"C:\Users\danielelder\Desktop\dump\20210507\lost_memories\신규 용어_확인 필요.xlsx"
current_glossary_2 = r"C:\Users\danielelder\Desktop\dump\Crusade\termbase\RO_combined_2.xlsx"

ignore_list = '게,번,란,회,나가,페르,제작,제련,염,괴'

if __name__=='__main__':

    start_time = time.time()
    gc = GlossaryChecker(
        current_sdlxliff, 
        current_glossary_2, 
        ignore_list    
    )
    result = gc.check()
    from pprint import pprint as pp
    pp(result)
    end_time = time.time()
    print(f"Duration: {end_time - start_time} seconds")

# add the above lines for glossary checking __doc__ as a example.
# show the most common problems found, to be used for filling the ignost_list (because they are likely false positives.)
# add decouple for test files so they are not all over the place (or make a json config file, or find out how config files are handled by other packages.)
# make output selection function (print to screen, make csv or excel, or both)
# need something to show the progress (? out of ?? segments searched.)
# mid is still not picking up correctly
# make a function that checks for a specific word or words
# ability to distinguish different apostrphes
# what if there are two glossary terms in one segment that need to be checked? (already doing this. Just needs a test set up to make sure.)
