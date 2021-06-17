from core.loader import Loader
import time

test_sdlxliff = r"tests/testdata/rok_const.sdlxliff"
test_glossary = r"tests/testdata/excel_glossary.xlsx"

current_sdlxliff = r"C:\Users\danielelder\J002_2021 The Lost Memories_KO2EN2PTBR_Additional\en-US"
current_glossary = r"C:\Users\danielelder\Desktop\dump\20210507\lost_memories\신규 용어_확인 필요.xlsx"
current_glossary_2 = r"C:\Users\danielelder\Desktop\dump\Crusade\termbase\RO_combined_2.xlsx"
glossary_dir = r"C:\Users\danielelder\Desktop\dump\20210507\lost_memories"

ignore_list = '게,란,회,나가,페르,제작,제련,염,괴,설정,보상,확인,?,강화,요한,링,립,침묵,추가,해달,월드맵,철,크로,완료,미니맵,꿀,북,시작,알,돌,셀,로그,스킬,카드,상자,책,보우,활,상자,직업,능력치,힐,떡,실패,안식,브륀힐트,모로코,모로크,사과'

if __name__=='__main__':

    start_time = time.time()

    loaded = Loader(
        current_sdlxliff, 
        current_glossary, 
        ignore_list,
        # writer="excel"
        )

    from pprint import pprint as pp

    # check glossary
    # for result in loaded.check_glossary():
    #     pp(result[1])
    

    # check length
    for result in loaded.check_length(source_min = 20):
        pp(result)
        print(f"total {len(result)} found.")


    # filter
    # for result in loaded.rfilter(source='프론테라', target='^((?!Prontera).)*$'):
    #     pp(result)

    
    
    
    end_time = time.time()
    print(f"Duration: {end_time - start_time} seconds")


# get random samplings for qa (doesn't trados already have this?)
# why is midgard getting false positives?
# implement multiprocessing for rfilter
# make tests to ensure sdlxliff and glossary are imported correctly, i.e. single and multiple files
# add decouple for test files so they are not all over the place (or make a json config file, or find out how config files are handled by other packages.)
# make documentation about output selection
# ability to distinguish different apostrphes
