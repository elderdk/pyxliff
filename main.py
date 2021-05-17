from core.loader import Loader
import time

test_sdlxliff = r"tests/testdata/rok_const.sdlxliff"
test_glossary = r"tests/testdata/excel_glossary.xlsx"

current_sdlxliff = r"C:\Users\danielelder\Desktop\dump\20210507\lost_memories\LanguageQuest_2021.04.16.ver.xlsx.sdlxliff"
current_glossary = r"C:\Users\danielelder\Desktop\dump\20210507\lost_memories\신규 용어_확인 필요.xlsx"
current_glossary_2 = r"C:\Users\danielelder\Desktop\dump\Crusade\termbase\RO_combined_2.xlsx"
glossary_dir = r"C:\Users\danielelder\Desktop\dump\20210507\lost_memories"

ignore_list = '게,번,란,회,나가,페르,제작,제련,염,괴,설정,보상,확인,?,강화,요한,링,립,침묵,추가,해달,월드맵,철,크로,완료,미니맵,꿀,북,시작,알,돌,셀,로그,스킬,카드,상자,책,보우,활,상자,직업,능력치,힐,떡,실패,안식,브륀힐트,모로코,모로크,사과'

if __name__=='__main__':

    start_time = time.time()

    loaded = Loader(
        current_sdlxliff, 
        current_glossary, 
        ignore_list
        )

    for _ in loaded.glossary_check():
        pass
    
    end_time = time.time()
    print(f"Duration: {end_time - start_time} seconds")


# make tests to ensure sdlxliff and glossary are imported correctly, i.e. single and multiple files
# find target segments with significant discrepancy with the source in terms of character length

# add decouple for test files so they are not all over the place (or make a json config file, or find out how config files are handled by other packages.)
# make output selection function (print to screen, make csv or excel, or both)
# make a function that checks for a specific word or words (using regex)
# ability to distinguish different apostrphes
