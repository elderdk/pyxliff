from glossary import GlossaryChecker

import glob
test_sdlxliff = glob.glob('./pyxliff/tests/testdata/*.sdlxliff')[0]
test_glossary = './pyxliff/tests/testdata/excel_glossary.xlsx'

current_sdlxliff = r"C:\Users\danielelder\Desktop\dump\lost_memories_update\0_Source\Studio\en-US\LanguageQuest_2021.04.16.ver.xlsx.sdlxliff"
current_glossary = r"C:\Users\danielelder\Desktop\dump\20210507\lost_memories\신규 용어_확인 필요.xlsx"
current_glossary_2 = r"C:\Users\danielelder\Desktop\dump\Crusade\termbase\RO_combined_2.xlsx"

ignore_list = '게,번,란'

if __name__=='__main__':

    gc = GlossaryChecker(
        current_sdlxliff, 
        current_glossary, 
        ignore_list    
    )
    gc.check()


# make ignore list capability
# make output selection function (print to screen, make csv or excel, or both)
# add threading or multiprocess to make it faster ()
# mid is still not picking up correctly
# make a function that checks for a specific word or words
# ability to distinguish different apostrphes
# what if there are two glossary terms in one segment that need to be checked? (already doing this. Just needs a test set up to make sure.)
# make a filtering function e.g.) produce segments that contain XXX and/or YYY.
