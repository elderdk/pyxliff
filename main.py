from core.loader import Loader
import time

test_sdlxliff = r"tests/testdata/rok_const.sdlxliff"
test_glossary = r"tests/testdata/excel_glossary.xlsx"

current_sdlxliff = r"C:\Users\danielelder\Desktop\dump\lost_memories_update\0_Source\Studio\en-US"
current_glossary = r"C:\Users\danielelder\Desktop\dump\20210507\lost_memories\신규 용어_확인 필요.xlsx"
current_glossary_2 = r"C:\Users\danielelder\Desktop\dump\Crusade\termbase\RO_combined_2.xlsx"

ignore_list = '게,번,란,회,나가,페르,제작,제련,염,괴,설정,보상,확인,?,강화,요한,링,립,침묵,추가,해달,월드맵,철,크로,완료,미니맵,꿀,북,시작,알,돌,셀,로그,스킬,카드,상자,책,보우,활,상자,직업,능력치,힐,떡,실패,안식,브륀힐트,모로코,모로크,사과'

if __name__=='__main__':

    start_time = time.time()

    loaded = Loader(
        current_sdlxliff, 
        current_glossary, 
        ignore_list
        )

    for _ in loaded.check():
        pass
    
    end_time = time.time()
    print(f"Duration: {end_time - start_time} seconds")


# find target segments with significant discrepancy with the source in terms of character length
# support for multiple glossaries and multiple sdlxliffs
# add the above lines for glossary checking __doc__ as a example.
# show the most common problems found, to be used for filling the ignost_list (because they are likely false positives.)
# add decouple for test files so they are not all over the place (or make a json config file, or find out how config files are handled by other packages.)
# make output selection function (print to screen, make csv or excel, or both)
# make a function that checks for a specific word or words
# ability to distinguish different apostrphes
